# Actichat

### Description
A chat app that allows users to create rooms and chat with each other. Users can also send links to each other so they have easy access to them.

### How to use

**Using Docker**
```bash
docker-compose up
```
visit localhost:3000

**Using Python**
```bash
pip install -r requirements.txt
python3 app.py
```
visit localhost:3000

# Environment Variables
- **SECRET_KEY**: secret key for flask
- **EVENTLET_HUB**: eventlet hub to use (poll or epoll)
- **FLASK_ENV**: flask environment (production or development)
- **FLASK_APP**: flask app to run (app.py)
