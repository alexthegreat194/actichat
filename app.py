from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret ;)'

socketio = SocketIO(app)

codes = [1234]


# Sockets

@socketio.on('hello')
def handle_connect(data):
    print('received json: ' + str(data))
    for i in range(5):
        emit('message', 'Hello!')

@socketio.on('message')
def handle_message(data):
    print('received json: ' + str(data))
    emit('message', data)

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
 