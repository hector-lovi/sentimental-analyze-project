from pymongo import MongoClient
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity as distance
import numpy as np
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()


class mObject():
    def __init__(self):
        self.myclient = MongoClient(
            os.getenv("mdb_url"))
        self.mydb = self.myclient.get_database()
        self.col_users = self.mydb['users']
        self.col_chats = self.mydb['chats']

    def user_id(self):
        '''
        Revisa si el id del usuario existe o no.
        Crea un id user único.
        '''
        # Lista de id users únicos
        us_id = self.col_users.distinct('_id')
        if us_id == []:
            return 0
        else:
            return max(us_id) + 1

    def user_name(self, username):
        '''
        Revisa si el nombre de usuario existe o no.
        '''
        us_name = self.col_users.distinct('name')
        if username in us_name:
            return 0
        else:
            return 1

    def createUser(self, username):
        '''
        Añade un usuario en la colección users.
        '''
        if self.user_name(username) == 1:
            userInfo = {
                '_id': self.user_id(),
                'name': username
            }
            self.col_users.insert_one(userInfo)
            return self.user_id()
        else:
            raise NameError(f'El nombre {username} ya se encuentra registrado')

    def chat_id(self):
        '''
        Revisa si el id del chat existe o no.
        Crea un id chat único.
        '''
        ch_id = self.col_chats.distinct('_id')
        if ch_id == []:
            return 1000
        else:
            return max(ch_id) + 1

    def createChat(self, name_chat):
        '''
        Añade un chat a la colección chats.
        '''
        new_chat = {
            '_id': self.chat_id(),
            'name': name_chat
        }
        self.col_chats.insert_one(new_chat)
        return (self.chat_id()) - 1

    def adduser_chat(self, chat_id, adduser):
        '''
        Comprueba previamente si el usuario existe en la colección users.
        Añade usuarios a un chat concreto.
        '''
        # Lista de chats id únicos
        ch_id = self.col_chats.distinct('_id')
        if int(chat_id) not in ch_id:
            raise ValueError(f'El chat con id {chat_id} no existe')

        # Lista de users name únicos
        us_name = self.col_users.distinct('name')
        if adduser not in us_name:
            raise NameError(f'El usuario {adduser} no existe')

        # id de usuario concreto
        id_adduser = list(self.col_users.find(
            {'name': adduser}, {'name': 0}))
        id_n = [v for d in id_adduser for k, v in d.items()][0]

        self.col_chats.update({'_id': int(chat_id)}, {
            '$push': {'users': int(id_n)}})
        return chat_id

    def addtext_chat(self, chat_id, user, message):
        '''
        Comprueba previamente si el chat existe en la colección chats.
        Añade texto a un chat concreto.
        '''
        # Lista de chats id únicos
        ch_id = self.col_chats.distinct('_id')
        if int(chat_id) not in ch_id:
            raise ValueError(f'El chat con id {chat_id} no existe')

        # Lista de users name únicos
        us_name = self.col_users.distinct('name')
        if user not in us_name:
            raise NameError(f'El usuario{user} no existe')

        # Lista de usuarios participantes únicos de un chat concreto
        ch_us = set(self.col_chats.find({'_id': int(chat_id)}, {
            '_id': 0, 'users': 1}))
        id_us = list(self.col_users.find({'name': user}, {
            'name': 0}))
        id_users = [v for d in id_us for k, v in d.items()][0]
        if id_users not in ch_us:
            raise NameError(f'El usuario {user} no se encuentra en el chat')

        self.col_chats.update({'_id': int(chat_id)}, {
            '$push': {'content': {'user': int(id_us), 'text': str(message)}}})
        return f'Mensaje añadido al chat {chat_id} con éxito'

    def alltext_chat(self, chat_id):
        '''
        Muestra todos los mensajes de un chat específico.
        '''
        messages = list(self.col_chats.find({'_id': int(chat_id)}, {
            '_id': 0, 'content': 1}))
        text = messages[0]
        return text

    def analyze_chat(self, chat_id):
        '''
        Realiza un análisis de sentimiento de un chat específico.
        '''
        text = self.alltext_chat(chat_id)['content']
        t = ' '.join([d['text'] for d in text])
        s = SentimentIntensityAnalyzer()
        result = s.polarity_scores(t)
        return result

    def recommender(self, docs):
        '''
        Recomendador de episodios en función de los parámetros descritos por el usuario.
        '''
        # Lista de todos los id chats de la colección chats
        c_id = self.col_chats.distinct('_id')
        for _id in c_id:
            all_text = ''
            for extract in self.alltext_chat(_id)['content']:
                text = ' '.join([extract['text']])
                all_text += text

            docs = {_id: all_text}

        count_vectorizer = CountVectorizer()
        sparse_matrix = count_vectorizer.fit_transform(docs.values())
        doc_term_matrix = sparse_matrix.todense()
        df = pd.DataFrame(doc_term_matrix,
                          columns=count_vectorizer.get_feature_names(),
                          index=docs.keys())
        similarity_matrix = distance(df, df)
        sim_df = pd.DataFrame(
            similarity_matrix, columns=docs.keys(), index=docs.keys())
        np.fill_diagonal(sim_df.values, 0)
        return sim_df.idxmax().head(3)
