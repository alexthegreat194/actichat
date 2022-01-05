from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret ;)'

socketio = SocketIO(app)

@socketio.on('hello')
def handle_connect(data):
    print('received json: ' + str(data))

@socketio.on('message')
def handle_message(data):
    print('received json: ' + str(data))
    send(data)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

 