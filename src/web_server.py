import random
import string
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Routes
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/join', methods=['GET'])
def join():
    return render_template('join.html')

@app.route('/join/<code>', methods=['GET'])
def join_code(code):
    return render_template('join.html', code=code)

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
    if name == '':
        name = 'Anonymous'
    
    return redirect(url_for('chat_join') + f"?code={code}&name={name}", code=307) #sends as post
