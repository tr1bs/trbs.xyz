from flask import Flask, Response, request, redirect, jsonify, url_for, send_file, render_template, session, abort, Markup, json
import os
from flask_cors import CORS
from datetime import datetime, date, timedelta
import json
from flask_login import LoginManager, current_user, login_user, login_required, logout_user, UserMixin
import sys
try:
    import pyAesCrypt
except Exception as e:
    print(e)

from api import db
from api import utils


"""

This architecture is interesting because its a "fat" version of serving html over wire
There are many ways but sending vue is the most productive and I won't need jwt
Can split to own front end when I will need advanced state
Can use Vue/Next for that
Theoretically I could write any type of client to consume this backend w jwt if split
Native can consume some api somehow
Regardless of all of this I think the main point in RAD is productivity
As long as the meat of the api is data first then you open up the doors to whatever
This on vercel is the cleanest minimal structure w/ ci/cd

todo: 
    use guide on hub to auto generate keys/wallet
    pool connections in psycopg
    convert print to log
    todo grabber
"""



app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/static")
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.secret_key = os.getenv('SHHH')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=2)

@login_manager.user_loader
def load_user(user_id):
    u = db.select_user_id(user_id)
    if u:
        return db.User(u[0], u[1], u[2], u[3])
    else:
        return False


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('settings.html')


@app.route('/error', methods=['GET', 'POST'])
def error():
    return render_template('error.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        r = db.register_user(request)        
        if r["success"]:
            return redirect('/login')
        else:
            # should flash here
            return render_template('error.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        if current_user.is_authenticated: return redirect('/')
        # todo: add email support

        username = request.values.get('username')
        password = request.values.get('password')
        data = None
        if username != None:      
            try:
                data = db.select_user(username) # todo: sanitize this
                # print(data)
            except Exception as e:
                # pass to exception handler
                print('error: ', str(e))
            

            if data == []:
                print('error: user is not registered')

            # print(data)
            user_id = data[0]
            hash = data[3]
            username = data[1]
            email = data[2]
            # todo: add support for new user fields here
            # todo: add retry
            if db.check_password_hash(hash, password):

                session['user_id'] = user_id
                session['username'] = username
                session['email'] = email

                wif = utils.create_wallet()

                user = db.User(user_id, username, email, wif)
                login_user(user)
                print('logged in: ', username)                

                return redirect('/')
            else:
                # redirect / return error, or flash
                return redirect('/error')

        else:
            return redirect('/error')


@app.route('/logout', methods=['POST'])
def logout():
    logout_user()    
    return jsonify(**{'result': 200, 'data': {'message': 'logout success'}})


@app.route('/user_info', methods=['GET'])
def user_info():
    if current_user.is_authenticated:
        resp = {"result": 200,
                "data": current_user.to_json()}
    else:
        resp = {"result": 401,
                "data": {"message": "user no login"}}
    return jsonify(**resp)


@app.route('/user_settings', methods=['GET', 'POST'])
def user_settings():
    if current_user.is_authenticated:
        if request.method == 'GET':
            print('getting here')
            u = db.select_user(current_user.username)
            if not u[5]: 
                r = {} 
            else:
                r = u[5]
            
            return r, 200

        if request.method == 'POST':
            r = request.get_json() # can return jsonify
            q = "UPDATE users SET settings='" + json.dumps(r) + "' WHERE id = " + str(current_user.get_id()) # fix this later
            pkg = db.update(q)

            return jsonify(pkg)

    else:
        resp = {"result": 401, "data": {"message": "user no login"}}
    return jsonify(**resp)

