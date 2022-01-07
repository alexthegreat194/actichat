from datetime import datetime
from os import name
import random
import string

from flask import Flask, render_template, url_for, request, redirect
from flask_socketio import SocketIO, emit, send


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret ;)'

socketio = SocketIO(app)

clients = {}

# Sockets
@socketio.on('client_connect')
def connect(data):
    print('received json: ' + str(data))
    clients[request.sid] = data['code']
    print(clients)

@socketio.on('disconnect')
def disconnect():
    print('client disconnected: ' + str(request.sid))
    del clients[request.sid]

@socketio.on('message')
def handle_message(data):
    print('received json: ' + str(data))
    keys = clients.keys()
    clients_to_send = []
    for key in keys:
        if clients[key] == data['code']:
            clients_to_send.append(key)
    print('Sending to clients: ' + str(clients_to_send))
    emit('message', data, broadcast=True, rooms=clients_to_send)


# Routes
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/join', methods=['GET'])
def join():
    return render_template('join.html')

@app.route('/join', methods=['POST'])
def join_post():
    data = {
        'name': request.form.get('name'),
        'code': request.form.get('code')
    }
    if data['name'] == '':
        data['name'] = 'Anonymous'
    return redirect(url_for('chat_join') + f"?code={data['code']}&name={data['name']}", code=307) #sends as post
    

@app.route('/chat', methods=['GET'])
def chat():
    return redirect(url_for('join'))

@app.route('/chat', defaults={'name':'Anonymous', 'code': ''}, methods=['POST'])
def chat_join(name, code):
    name = request.args.get('name')
    code = request.args.get('code')
    return render_template('chat.html', code=code, name=name)

@app.route('/create', methods=['GET'])
def create():
    return render_template('create.html')

@app.route('/create', methods=['POST'])
def create_post():
    name = request.form.get('name')
    code = ""
    for i in range(8):
        code += random.choice(string.ascii_lowercase)
    print('new code: ' + str(code) + " from " + str(name))
    if name != '':
        name = 'Anonymous'
    
    return redirect(url_for('chat_join') + f"?code={code}&name={name}", code=307) #sends as post

