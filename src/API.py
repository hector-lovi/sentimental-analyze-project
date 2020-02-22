from flask import Flask, request
from mongoReq import createUser

app = Flask(__name__)


@app.route('/')
def start():
    print('Bienvenid@!! Si tienes dudas de como usar esta API consulta el archivo README.md')


@app.route('/user/create/<username>')
def addUser(username):
    return createUser(username)


app.run("0.0.0.0", 4999, debug=True)
