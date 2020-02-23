from flask import Flask, request
from mRequest import mongoFunc

app = Flask(__name__)

mon = mongoFunc()


@app.route('/help')
def start():
    return 'Bienvenid@!! Si tienes dudas de como usar esta API consulta el archivo README.md'


@app.route('/user/create/<username>')
def addUser(username):
    query = mon.createUser(username)
    return f'El usuario {username} con id {query} ha sido registrado con éxito'


@app.route('/chat/create')
def create_chat(*args):
    name_chat = request.args.get(key='name')
    query = mon.createChat(name_chat)
    return f'El chat {name_chat} con id {query} ha sido creado con éxito'


@app.route('/chat/<chat_id>/adduser')
def user_to_chat(chat_id, *args):
    addUser = request.args.get(key='user')
    query = mon.adduser_chat(chat_id, addUser)
    return f'El usuario {addUser} ha sido añadido al chat {query}'


@app.route('/chat/<chat_id>/addmessage')
def message_to_chat(chat_id, *args):
    user = request.args.get(key='user')
    message = request.args.get(key='text')
    query = mon.addtext_chat(chat_id, user, message)
    return query


@app.route('/chat/<chat_id>/list')
def all_message(chat_id):
    query = mon.alltext_chat(chat_id)
    return query


@app.route('/chat/<chat_id>/sentiment')
def sentiment_chat(chat_id):
    query = mon.analyze_chat(chat_id)
    print('EOOOOOOOOOO')
    return query


app.run("0.0.0.0", 4999, debug=True)
