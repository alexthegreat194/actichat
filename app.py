import os
import logging

# Must be before other imports for production async workers
async_mode = os.environ.get('ASYNC_MODE', 'threading')
if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()

from src.web_server import app
from src.socket_server import socketio

secret_key = os.environ.get('SECRET_KEY')
if not secret_key:
    raise ValueError("SECRET_KEY environment variable must be set in production")
app.config['SECRET_KEY'] = secret_key

app.logger.setLevel(logging.INFO)

if __name__ == '__main__':
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    socketio.run(app, host='0.0.0.0', port=3000, debug=debug, allow_unsafe_werkzeug=True)