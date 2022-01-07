from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret ;)'

socketio = SocketIO(app)

codes = [1234]
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
        return redirect(url_for('chat_join', code=data['code']))
    else:
        return redirect(url_for('chat_join', code=data['code'], name=data['name']))

@app.route('/chat', methods=['GET'])
def chat():
    return redirect(url_for('join'))

@app.route('/chat/<code>', defaults={'name':None}, methods=['GET'])
@app.route('/chat/<code>/<name>', methods=['GET'])
def chat_join(code, name):
    if code == None:
        code = "Anonymous"
    
    return render_template('chat.html', code=code, name=name)
 