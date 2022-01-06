from flask import Flask, render_template, url_for, request, redirect
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret ;)'

socketio = SocketIO(app)

# Sockets

@socketio.on('hello')
def handle_connect(data):
    print('received json: ' + str(data))
    for i in range(10):
        emit('message', 'Hello!')

@socketio.on('message')
def handle_message(data):
    print('received json: ' + str(data))
    send(data)


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
    return redirect(url_for('chat_join', code=data['code']))

@app.route('/chat', methods=['GET'])
def chat():
    pass

@app.route('/chat/<code>', methods=['GET'])
def chat_join(code):
    return redirect(url_for('index'))
 