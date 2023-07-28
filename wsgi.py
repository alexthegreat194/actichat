import eventlet
from eventlet import wsgi
from app import app

import dotenv
dotenv.load_dotenv()

wsgi.server(eventlet.listen(("0.0.0.0", 3000)), app)