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
        self.col_episodes = self.mydb['episodes']

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

    def episode_id(self):
        '''
        Revisa si el id del episode existe o no.
        Crea un id episode único.
        '''
        ep_id = self.col_episodes.distinct('_id')
        if ep_id == []:
            return 1000
        else:
            return max(ep_id) + 1

    def createepisode(self, name_episode):
        '''
        Añade un episode a la colección episodes.
        '''
        new_episode = {
            '_id': self.episode_id(),
            'name': name_episode
        }
        self.col_episodes.insert_one(new_episode)
        return (self.episode_id()) - 1

    def adduser_episode(self, episode_id, adduser):
        '''
        Comprueba previamente si el usuario existe en la colección users.
        Añade usuarios a un episode concreto.
        '''
        # Lista de episodes id únicos
        ep_id = self.col_episodes.distinct('_id')
        if int(episode_id) not in ep_id:
            raise ValueError(f'El episode con id {episode_id} no existe')

        # Lista de users name únicos
        us_name = self.col_users.distinct('name')
        if adduser not in us_name:
            raise NameError(f'El usuario {adduser} no existe')

        # id de usuario concreto
        id_adduser = list(self.col_users.find(
            {'name': adduser}, {'name': 0}))
        id_n = [v for d in id_adduser for k, v in d.items()][0]

        self.col_episodes.update({'_id': int(episode_id)}, {
            '$push': {'users': int(id_n)}})
        return episode_id

    def addtext_episode(self, episode_id, user, message):
        '''
        Comprueba previamente si el episode existe en la colección episodes.
        Añade texto a un episode concreto.
        '''
        # Lista de episodes id únicos
        ep_id = self.col_episodes.distinct('_id')
        if int(episode_id) not in ep_id:
            raise ValueError(f'El episode con id {episode_id} no existe')

        # Lista de users name únicos
        us_name = self.col_users.distinct('name')
        if user not in us_name:
            raise NameError(f'El usuario{user} no existe')

        # Lista de usuarios participantes únicos de un episode concreto
        ep_us = list(self.col_episodes.find({'_id': int(episode_id)}, {
            '_id': 0, 'users': 1}))
        ep_us = set(ep_us[0]['users'])
        id_us = list(self.col_users.find({'name': user}, {
            'name': 0}))
        id_user = [v for d in id_us for k, v in d.items()][0]
        if id_user not in ep_us:
            raise NameError(f'El usuario {user} no se encuentra en el episode')

        self.col_episodes.update({'_id': int(episode_id)}, {
            '$push': {'content': {'user': int(id_user), 'text': str(message)}}})
        return f'Mensaje añadido al episode {episode_id} con éxito'

    def alltext_episode(self, episode_id):
        '''
        Muestra todos los mensajes de un episode específico.
        '''
        messages = list(self.col_episodes.find({'_id': int(episode_id)}, {
            '_id': 0, 'content': 1}))
        text = messages[0]
        return text

    def analyze_episode(self, episode_id):
        '''
        Realiza un análisis de sentimiento de un episode específico.
        '''
        text = self.alltext_episode(episode_id)['content']
        t = ' '.join([d['text'] for d in text])
        s = SentimentIntensityAnalyzer()
        result = s.polarity_scores(t)
        return result

    def recommender(self, docs):
        '''
        Recomendador de episodios en función de los parámetros descritos por el usuario.
        '''
        # Lista de todos los id episodes de la colección episodes
        c_id = self.col_episodes.distinct('_id')
        for _id in c_id:
            all_text = ''
            for extract in self.alltext_episode(_id)['content']:
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
