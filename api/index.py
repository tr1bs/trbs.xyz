from flask import Flask, Response, request, redirect, jsonify, url_for, send_file, render_template, session, abort, Markup, json
import os
from flask_cors import CORS
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from datetime import datetime, date, timedelta
import json

from flask_login import LoginManager, current_user, login_user, login_required, logout_user, UserMixin
import sys
try:
    import pyAesCrypt
except Exception as e:
    print(e)



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

todo: pool connections in psycopg
    convert print to log
    todo grabber
"""



class User(object):
    def __init__(self, user_id, username, email):
        self.user_id = user_id
        self.username= username
        self.authenticated = True
        self.email = email

    def is_active(self): return True

    def get_id(self): return self.user_id

    def is_authenticated(self): return self.authenticated

    def is_anonymous(self): return False   


connection = "dbname={} user={} host={} password={} port='5432'".format(os.getenv('PGDATABASE'), os.getenv('PGUSER'), os.getenv('PGHOST'), os.getenv('PGPASSWORD'))

def select(sql):
    conn = psycopg2.connect(connection)
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    conn.close()
    print('selected data successfully: ', sql)
    if data:
        data = data[0]
        return data
    else:
        return False


def select_user(username):
    sql = "SELECT * from users where username = '" + username + "';"
    return select(sql)


def select_user_id(id):
    sql = "SELECT * from users where id = '" + str(id) + "';"
    return select(sql)


def insert(sql):
    try: 
        conn = psycopg2.connect(connection)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        return {"success": True, "message": "data inserted successfully" }
    except Exception as e:
        print(e)
        return {"success": False, "message": str(e)}


def register_user(request):
    username = request.values.get('username')
    password = request.values.get('password')
    email = request.values.get('email')
    data = select_user(username)

    if not data:
        # todo: sanitize this
            # add bsv wallet
        generate_user = '''insert into users (username, email, hash) values ('{}', '{}', '{}') ON CONFLICT DO NOTHING;
                        '''.format(username, email, generate_password_hash(password), username)

        r = insert(generate_user)
        return r

    else:
        return {"success": False, "message": "Failed registration"}
    


app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/static")
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.secret_key = os.getenv('SHHH')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=2)

@login_manager.user_loader
def load_user(user_id):
    u = select_user_id(user_id)
    return User(u[0], u[1], u[2])


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')


@app.route('/error', methods=['GET', 'POST'])
def error():
    return render_template('error.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        r = register_user(request)
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

        if username != None:      
            try:
                data = select_user(username) # todo: sanitize this
            except Exception as e:
                # pass to exception handler
                print('error: ', str(e))

            if data == []:
                print('error: user is not registered')

            print(data)
            user_id = data[0]
            hash = data[3]
            username = data[1]
            email = data[2]
            # todo: add support for new user fields here
            # todo: add retry
            if check_password_hash(hash, password):

                session['user_id'] = user_id
                session['username'] = username
                session['email'] = email

                user = User(user_id, username, email)            
                login_user(user)
                print('logged in')

                return redirect('/')
            else:
                # redirect / return error, or flash
                return redirect('/error')

        else:
            return redirect('/error')


@app.route('/about')
def about():
    return 'About'
