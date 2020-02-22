from pymongo import MongoClient

myclient = MongoClient("mongodb://localhost:27017/sentimental-analyze")
mydb = myclient.get_database()
col_users = mydb['users']
col_chats = mydb['chats']


def user_id():
    q = {'id_user': {'$exists': True}}
    query = list(col_users.find(q, {'_id': 0, 'id_user': 1}))
    val_id = []
    for e in query:
        for k, v in e.items():
            val_id.append(v)
    if val_id == []:
        return 0
    else:
        return max(val_id) + 1


def createUser(username):
    id_user = user_id()
    userInfo = {
        'id_user': id_user,
        'name': username
    }

    col_users.insert_one(userInfo)
    return f'User {username} created'


def chat_id():
    q = {'id_chat': {'$exists': True}}
    query = list(col_chats.find(q, {'_id': 0, 'id_chat': 1}))
    val_id = []
    for e in query:
        for k, v in e.items():
            val_id.append(v)
    if val_id == []:
        return 1000
    else:
        return max(val_id) + 1


def createChat(content):
    id_chat = chat_id()

    userInfo = {
        'id_chat': id_chat,
        'content': content
    }

    col_chats.insert_one(userInfo)
    print(f'chat {id_chat} created')
    return 'Todo puto OK'
