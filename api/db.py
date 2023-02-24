import sys
import os
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from api import utils

class User(object):
    def __init__(self, user_id, username, email, wif):
        self.user_id = user_id
        self.username = username
        self.authenticated = True
        self.email = email
        self.wif = wif
        self.settings = ''

    def to_json(self): return { "username": self.username, "email": self.email, "wif": self.wif }

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


def update(sql):
    try: 
        conn = psycopg2.connect(connection)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        return {"success": True, "message": "data updated successfully" }
    except Exception as e:
        print(e)
        return {"success": False, "message": str(e)}


def register_user(request):
    username = request.values.get('username')
    password = request.values.get('password')
    email = request.values.get('email')
    data = select_user(username)

    if not data:
        wif = utils.create_wallet()
        # todo: sanitize this
            # add bsv wallet
        generate_user = '''insert into users (username, email, hash, wif) values ('{}', '{}', '{}', '{}') ON CONFLICT DO NOTHING;
                        '''.format(username, email, generate_password_hash(password), wif)

        r = insert(generate_user)
        return r

    else:
        return {"success": False, "message": "Failed registration"}