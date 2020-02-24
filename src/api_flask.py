from flask import Flask, request
from mRequest import mObject
from jsonErrorHandler import jsonErrorHandler
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@jsonErrorHandler
@app.route('/help')
def start():
    return 'Bienvenid@!! Si tienes dudas de como usar esta API consulta el archivo README.md'


@jsonErrorHandler
@app.route('/user/create/<username>')
def addUser(username):
    m.createUser(username)
    return f'El usuario {username} ha sido registrado con éxito'


@jsonErrorHandler
@app.route('/chat/create')
def create_chat():
    name_chat = request.args.get(key='name')
    query = m.createChat(name_chat)
    return f'El chat {name_chat} con id {query} ha sido creado con éxito'


@jsonErrorHandler
@app.route('/chat/<chat_id>/adduser')
def user_to_chat(chat_id):
    addUser = request.args.get(key='user')
    query = m.adduser_chat(chat_id, addUser)
    return f'El usuario {addUser} ha sido añadido al chat {query}'


@jsonErrorHandler
@app.route('/chat/<chat_id>/addmessage')
def message_to_chat(chat_id):
    user = request.args.get(key='user')
    message = request.args.get(key='text')
    query = m.addtext_chat(chat_id, user, message)
    return query


@jsonErrorHandler
@app.route('/chat/<chat_id>/list')
def all_message(chat_id):
    query = m.alltext_chat(chat_id)
    return query


@jsonErrorHandler
@app.route('/chat/<chat_id>/sentiment')
def sentiment_chat(chat_id):
    query = m.analyze_chat(chat_id)
    return query


@jsonErrorHandler
@app.route('/chat/recommend')
def reco():
    docs = request.args.get(key='description')
    query = m.recommender(docs)
    return f'Capítulos recomendados = {query}'


m = mObject()
app.run('0.0.0.0', os.getenv("port"), debug=True)
