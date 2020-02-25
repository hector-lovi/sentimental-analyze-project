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
    return '¡¡Bienvenid@!! Para cualquier duda lee las instrucciones en el archivo README.md :)'


@jsonErrorHandler
@app.route('/user/create/<username>')
def addUser(username):
    m.createUser(username)
    return f'El usuario {username} ha sido registrado con éxito'


@jsonErrorHandler
@app.route('/episode/create')
def create_episode():
    name_episode = request.args.get(key='name')
    query = m.createepisode(name_episode)
    return f'El episode {name_episode} con id {query} ha sido creado con éxito'


@jsonErrorHandler
@app.route('/episode/<episode_id>/adduser')
def user_to_episode(episode_id):
    addUser = request.args.get(key='user')
    query = m.adduser_episode(episode_id, addUser)
    return f'El usuario {addUser} ha sido añadido al episode {query}'


@jsonErrorHandler
@app.route('/episode/<episode_id>/addmessage')
def message_to_episode(episode_id):
    user = request.args.get(key='user')
    message = request.args.get(key='text')
    query = m.addtext_episode(episode_id, user, message)
    return query


@jsonErrorHandler
@app.route('/episode/<episode_id>/list')
def all_message(episode_id):
    query = m.alltext_episode(episode_id)
    return query


@jsonErrorHandler
@app.route('/episode/<episode_id>/sentiment')
def sentiment_episode(episode_id):
    query = m.analyze_episode(episode_id)
    return query


@jsonErrorHandler
@app.route('/episode/recommend')
def reco():
    docs = request.args.get(key='description')
    query = m.recommender(docs)
    return f'Capítulos recomendados = {query}'


m = mObject()
app.run('0.0.0.0', os.getenv("port"), debug=True)
