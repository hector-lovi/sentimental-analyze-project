from pymongo import MongoClient
import jsonErrorHandler
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class mongoFunc():
    def __init__(self):
        self.myclient = MongoClient(
            "mongodb://localhost:27017/sentimental-analyze")
        self.mydb = self.myclient.get_database()
        self.col_users = self.mydb['users']
        self.col_chats = self.mydb['chats']

    @jsonErrorHandler
    def user_id(self):
        us_id = self.col_users.distinct('_id')
        if us_id == []:
            return 0
        else:
            return max(us_id) + 1

    @jsonErrorHandler
    def user_name(self, username):
        us_name = self.col_users.distinct('name')
        if username in us_name:
            return 0
        else:
            return 1

    @jsonErrorHandler
    def createUser(self, username):
        if self.user_name(username) == 1:
            userInfo = {
                '_id': self.user_id(),
                'name': username
            }
            self.col_users.insert_one(userInfo)
            return self.user_id()
        else:
            raise NameError(f'El nombre {username} ya se encuentra registrado')

    @jsonErrorHandler
    def chat_id(self):
        ch_id = self.col_chats.distinct('_id')
        if ch_id == []:
            return 1000
        else:
            return max(ch_id) + 1

    @jsonErrorHandler
    def createChat(self, name_chat):
        new_chat = {
            '_id': self.chat_id(),
            'name': name_chat
        }
        self.col_chats.insert_one(new_chat)
        return self.chat_id

    @jsonErrorHandler
    def adduser_chat(self, chat_id, adduser):
        ch_id = self.col_chats.distinct('_id')
        if int(chat_id) not in ch_id:
            raise ValueError(f'El chat con id {chat_id} no existe')
        else:
            us_name = self.col_users.distinct('name')
        if adduser not in us_name:
            raise NameError(f'El usuario {adduser} no existe')
        else:
            id_adduser = list(self.col_users.find(
                {'name': adduser}, {'name': 0}))
            id_n = [v for d in id_adduser for k, v in d.items()][0]
            self.col_chats.update({'_id': int(chat_id)}, {
                                  '$push': {'users': int(id_n)}})
        return chat_id

    @jsonErrorHandler
    def addtext_chat(self, chat_id, user, message):
        ch_id = self.col_chats.distinct('_id')
        if int(chat_id) not in ch_id:
            raise ValueError(f'El chat con id {chat_id} no existe')
        else:
            us_name = self.col_users.distinct('name')
        if user not in us_name:
            raise NameError(f'El usuario{user} no existe')
        else:
            ch_us = self.col_chats.distinct('users')
            id_us = list(self.col_users.find(
                {'name': user}, {'name': 0}))
            id_us = [v for d in id_us for k, v in d.items()][0]
        if id_us not in ch_us:
            raise NameError(
                f'El usuario {user} no se encuentra en el chat')
        else:
            self.col_chats.update({'_id': int(chat_id)}, {
                                  '$push': {'content': {'user': int(id_us), 'text': str(message)}}})
        return f'Mensaje añadido al chat {chat_id} con éxito'

    @jsonErrorHandler
    def alltext_chat(self, chat_id):
        messages = list(self.col_chats.find({'_id': int(chat_id)}, {
            '_id': 0, 'content': 1}))
        text = messages[0]
        return text

    @jsonErrorHandler
    def analyze_chat(self, chat_id):
        text = self.alltext_chat(chat_id)['content']
        t = ' '.join([d['text'] for d in text])
        s = SentimentIntensityAnalyzer()
        result = s.polarity_scores(t)
        return result
