from flask import Flask, Response, request, redirect, jsonify, url_for, send_file, render_template, session, abort, Markup, json
import os
from flask_cors import CORS
from datetime import datetime, date, timedelta
import json
from flask_login import LoginManager, current_user, login_user, login_required, logout_user, UserMixin
import sys
import uuid
import shortuuid

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
        return db.User(u[0], u[1], u[2])
    else:
        return redirect('/register')


@app.route('/', methods=['GET'])
@login_required
def index():
    # can login check or redir
    if request.method == 'GET':
        print(current_user)        
        return render_template('index.html')



@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('settings.html')


@app.route('/error', methods=['GET', 'POST'])
def error():
    return render_template('error.html')

@app.route('/u/<username>', methods=['GET', 'POST'])
def get_user(username):
    return render_template('user.html')


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
        print(username)
        print(password)
        data = None
        if username != None:      
            try:
                data = db.select_user(username) # todo: sanitize this
                print(data)
            except Exception as e:
                # pass to exception handler
                print('error: ', str(e))
            

            if data == []:
                print('error: user is not registered')

            print(data)
            if data is not None and data:
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

                    # wif = utils.create_wallet() bsv wallet creation

                    user = db.User(user_id, username, email)
                    login_user(user)
                    print('logged in: ', username)                

                    return redirect('/')
                else:
                    # redirect / return error, or flash
                    return redirect('/error')
            else:
                print('invalid user') # flash to user here

        else:
            return redirect('/error')


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()    
    return jsonify(**{'result': 200, 'data': {'message': 'logout success'}})


# app.route('/u')
# app.route('/u/<username>')
# def dir_user():
#     return render_template('user.html')



@app.route('/api/v1/user_info', methods=['GET'])
def user_info():
    if current_user:
        if current_user.is_authenticated:
            resp = {"result": 200,
                    "data": current_user.to_json()}
        else:
            resp = {"result": 401,
                    "data": {"message": "user no login"}}

    else:
        resp = {"result": 401,
                "data": {"message": "user no login"}}
    return jsonify(**resp)


@app.route('/api/v1/user_settings', methods=['GET', 'POST'])
def user_settings():
    if current_user.is_authenticated:
        if request.method == 'GET':
            u = db.select_user(current_user.username)
            print(u)
            if not u[4]: 
                r = {
                    "username": u[1],
                    "settings": {}
                } 
            else:
                r = u[1]
                r = u[4]
                r = {
                    "username": u[1],
                    "settings": u[4]
                }
                # r['username'] = current_user.username
            
            return r, 200

        if request.method == 'POST':
            r = request.get_json() # can return jsonify
            q = "UPDATE users SET settings='" + json.dumps(r) + "' WHERE id = " + str(current_user.get_id()) # fix this later
            pkg = db.update(q)

            return jsonify(pkg)

    else:
        resp = {"result": 401, "data": {"message": "user no login"}}
    return jsonify(**resp)


@app.route('/api/v1/get_user/<username>', methods=['GET'])
@login_required
def public_user(username):
    if request.method == 'GET':
        print('getting public user')
        r = db.select_public_user(username)
        # print(r[0], r[1])
        pkg = {}        
        for idx, column in enumerate(r[1]):
            pkg[column] = r[0][idx]

        return json.dumps(pkg), 200


@app.route('/api/v1/get_authed_pub', methods=['GET'])
@login_required
def public_user_authed():
    if request.method == 'GET':
        if current_user.is_authenticated:
            username = current_user.username
            print('getting public user')
            r = db.select_public_user(username)
            # print(r[0], r[1])
            pkg = {}        
            for idx, column in enumerate(r[1]):
                pkg[column] = r[0][idx]

            return json.dumps(pkg), 200
        else:
            return 500


@app.route('/api/v1/add_user_wallet', methods=['POST'])
@login_required
def add_wallet():    
    if request.method == 'POST':        
        # print(session)
        print('getting public user')
        r = request.get_json() # can return jsonify
        print(r)    
        q = '''update dir set eth_wallet = '{}' where username = '{}'; '''.format(r['address'], r['username'])
        # sql = "UPDATE dir set address = '" + r['address'] + "' WHERE username = '" + r['username'] = "';"
        pkg = db.update(q)
        session['address'] = r['address'] 
        print(session)

        # return jsonify(pkg)
        return json.dumps(r), 200


@app.route('/api/v1/i/add', methods=['GET', 'POST'])
@login_required
def add_items():

    if request.method == 'POST':
        print('api - adding item')
        r = request.get_json()
        r['uuid'] = shortuuid.ShortUUID().random(length=16)
        columns = [*r.keys()]
        # print(columns)
        pkg = db.insert_item(columns, r)
        print(pkg)

        return jsonify(pkg)



@app.route('/i', methods=['GET', 'POST'])
@login_required
def items():
    return render_template('items.html')


@app.route('/i/<uuid>', methods=['GET', 'POST'])
@login_required
def item(uuid):
    return render_template('item.html')


@app.route('/i/add', methods=['GET', 'POST'])
@login_required
def add_item_form():
    if request.method == 'GET':
        return render_template('add_item.html')


@app.route('/i/u/<username>', methods=['GET'])
@login_required
def user_items(username):
    return render_template('user_items.html')


@app.route('/api/v1/i/get_all', methods=['GET'])
@login_required
def get_all_items():
    if request.method == 'GET':
        print('api - fetching items...')
        r = db.select_all_items() #can paginate this later
        pkg = {}
        for item in r:
            print(item, '\n')
        
        return json.dumps(r, default=utils.serialize_datetime), 200


@app.route('/api/v1/i/get_item/<uuid>', methods=['GET'])
@login_required
def get_item(uuid):
    if request.method == 'GET':
        print('api - fetching item...')
        r = db.select_single_item(uuid) #can paginate this later

        for item in r:
            print(item, '\n')
        
        return json.dumps(r, default=utils.serialize_datetime), 200


@app.route('/api/v1/i/u/<username>', methods=['GET'])
@login_required
def get_username_items(username):
    if request.method == 'GET':
        print('api - fetching user items...')
        r = db.select_user_items(username) # can paginate this later

        # print(r)
        for item in r:
            print(item, '\n')
        
        return json.dumps(r, default=utils.serialize_datetime), 200


@app.route('/api/v1/i/buy_item', methods=['POST'])
@login_required
def buy_item():
    if request.method == 'POST':
        print('api -- purchasing item...')        
        if current_user.authenticated:
            r = request.get_json()
            username = current_user.username
            # open request 

            # get user address



    # if request.method == 'POST':
    #     user = current_user.username
        # username = request.values.get('username')
        # password = request.values.get('password')


