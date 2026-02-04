import os
from flask import request
from flask_socketio import SocketIO, emit, join_room
from src.web_server import app

async_mode = os.environ.get('ASYNC_MODE', 'threading')
socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins="*")

# Sockets
@socketio.on('client_connect')
def connect(data):
    code = data['code']
    app.logger.info(f'Client {request.sid} joining room: {code}')
    join_room(code)

@socketio.on('disconnect')
def disconnect():
    app.logger.info(f'Client disconnected: {request.sid}')
    # Flask-SocketIO automatically removes clients from all rooms on disconnect

@socketio.on('message')
def handle_message(data):
    code = data['code']
    app.logger.info(f'Message to room {code}: {data}')
    emit('message', data, to=code)