
from flask import Flask
from flask_socketio import SocketIO
from passlib.hash import sha256_crypt
from mongoengine import connect
from database.db import add_user, find_user, add_file, add_unit, get_files, get_file_id, update_file
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
UPLOAD_FOLDER = "static/file/pdf/"
app.config['SECRET_KEY'] = 'socket_digital'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


try:
    connect('socket')
    print('connected socket')
except Exception as e:
    print('can not connect to db' + e)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@socketio.on('id')
def handle_connect(id):
    print('[{} connected]'.format(id))


@socketio.on('register')
def handle_register(data):
    data['password'] = sha256_crypt.hash(data['password'])
    try:
        add_user(data)
        socketio.emit('register success')
    except Exception as e:
        print(e)
        socketio.emit('register err')


@socketio.on('login')
def handle_login(data):
    user = find_user(data['email'], data['password'])
    if user:
        if sha256_crypt.verify(data['password'], user['password']):
            userR = {
                "id": str(user['id']),
                "name": user['name'],
                "email": user['email'],
                "age": user['age'],
                "address": user['address'],
                "isAdmin": user['isAdmin'],
                "roleUnit": user['roleUnit'],
            }
            socketio.emit('login success', userR)
        else:
            mess = 'Password incorrect'
            socketio.emit('login err', mess)
    else:
        mess = 'Email incorrect'
        socketio.emit('login err', mess)


@socketio.on('add-unit')
def handle_add_unit(data):
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    try:
        room_name = str(ts) + '.' + data['name'] + '.' + data['MST']
        data['room_name'] = room_name
        add_unit(data)
        join_room(room_name)
        socketio.emit('add unit success')
    except Exception as e:
        socketio.emit('add unit false')


@socketio.on('upload-file')
def upload_file(data, filename, last_modified):
    file_name = secure_filename(str(last_modified) + '-' + filename)
    destination = "/".join(["static/file/pdf", file_name])
    try:
        file = open(destination, 'wb')
        file.write(data)
        file.close()
        socketio.emit('upload-success', destination)
        print('saved file 96')
    except Exception as e:
        print(e)
        mess = 'Upload file failure'
        socketio.emit('upload-fail', mess)


@socketio.on('write-chunk')
def save_file(data, filename):
    file_name = secure_filename(filename)
    destination = "/".join(["static/file/pdf", file_name])
    file = open(destination, 'wb')
    file.write(data)
    file.close()


@socketio.on('add-file')
def handle_add_file(data):
    print('data', str(data))
    try:
        add_file(data)
        socketio.emit('Add file success')
    except Exception as e:
        print(e)
        mess = 'Add file failure'
        socketio.emit('add-file-fail', mess)


@socketio.on('list file')
def handle_get_all_file():
    try:
        files = get_files()
        listFile = []
        for i in files:
            dataRes = {
                "id": str(i['id']),
                "code": i['code'],
                "name": i['name'],
                "link": i['link'],
                "createFileAt": str(i['createFileAt']),
                "createFileBy": i['createFileBy'],
                "isSign": i['isSign'],
                "signFileAt": str(i['signFileAt']),
                "signFileBy": i['signFileBy'],
            }
            listFile.append(dataRes)
        socketio.emit('file res', listFile)
    except Exception as e:
        print(e)


@socketio.on('get file')
def get_file(data):
    try:
        file = get_file_id(data)
        dataR = {
            "id": str(file['id']),
            "code": file['code'],
            "name": file['name'],
            "link": file['link'],
            "createFileAt": str(file['createFileAt']),
            "createFileBy": file['createFileBy'],
            "isSign": file['isSign'],
            "signFileAt": str(file['signFileAt']),
            "signFileBy": file['signFileBy'],
        }
        socketio.emit('file with id', dataR)
    except Exception as e:
        print(e)


@socketio.on('sign file')
def sign_file(data):
    dt = str(datetime.now())
    data['link'] = "/".join(["static/file/pdf", data['link']])
    print(data)
    fileU = update_file(data['id'], data['isSign'], data['signFileBy'], data['link'], dt)
    socketio.emit('sign success')


if __name__ == '__main__':
    socketio.run(app, debug=True)
