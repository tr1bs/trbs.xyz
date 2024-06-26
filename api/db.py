import sys
import os
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from api import utils

from psycopg2.extras import Json
from psycopg2.extensions import AsIs, register_adapter

register_adapter(dict, Json)
'''
Schemas:
    Bio - text


    Class dir
        autoinc id
        username fkey
        bio
        tribs # gen in constructor ---what if change trib as distributed dao
        followers # gen in constructor (auto add)
        following?
        wallet # gen in connection event
        items # gen in constructor

    Class items
        uuid
        owner fkey username in dir
        owner address fkey address from dir @ username
        brand varchar
        colors jsonb
        created timestamp
        description varchar
        for_sale bool
        img jsonb
        materials jsonb
        name varchar
        price varchar
        reposted jsonb
        saved jsonb
        season varchar
        status varchar ['for sale', 'escrow', 'not for sale'] can prob turn this into index type later
        source_url varchar
        size varchar
        tags jsonb
        tribs jsonb
        tx jsonb
        transactions [ uuid of hist items ]

    Class items_activity
        item owner fkey items uuis
        creator
        type varchar ['listing', 'transaction']

    class hist
        - a history of all transactions

        uuid
        buyer
        seller
        ethscanTx
        datetime
        tx_hash
        going to need a referrer eventually

    class fufillment
        uuid
        buyer
        seller
        ethscan_tx
        hist_id
        datetime
        eventually this table will become 'escrow' and have a signatures trey (count -> items)
            - and an expiry for the tribunal







'''
class Public(object):
    def __init__(self, username, bio):
        self.username = username
        self.bio = bio
        # self.tribs = []
        # self.followers = ['admin']
        # self.following = []
        # self.image_url = ''

    def to_json(self): return { "username": self.username, "bio": self.bio, "followers": self.followers, "following": self.following, "image_url": self.image_url }




class User(object):
    def __init__(self, user_id, username, email):
        self.user_id = user_id
        self.username = username
        self.authenticated = True
        self.email = email
        self.settings = ''

    def to_json(self): return { "username": self.username, "email": self.email }

    def is_active(self): return True

    def get_id(self): return self.user_id

    def is_authenticated(self): return self.authenticated



connection = "dbname={} user={} host={} password={} port='5432'".format(os.getenv('PGDATABASE'), os.getenv('PGUSER'), os.getenv('PGHOST'), os.getenv('PGPASSWORD'))

def select(sql):
    conn = psycopg2.connect(connection, sslmode='require')
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

def select_with_columns(sql):
    conn = psycopg2.connect(connection, sslmode='require')
    cur = conn.cursor()
    cur.execute(sql)
    column_names = [desc[0] for desc in cur.description]
    data = cur.fetchall()
    cur.close()
    conn.close()
    print('selected data successfully: ', sql)
    print(data, '\n')
    if data:
        data = data[0]
        return data, column_names
    else:        
        return False


def select_with_columns_item(sql):
    conn = psycopg2.connect(connection, sslmode='require')
    cur = conn.cursor()
    cur.execute(sql)
    column_names = [desc[0] for desc in cur.description]
    data = cur.fetchall()
    cur.close()
    conn.close()
    print('selected data successfully: ', sql)
    # print(data, '\n')
    if data:        
        return data, column_names
    else:        
        return False 


def select_user(username):
    sql = "SELECT * from users where username = '" + username + "';"
    return select(sql)


def select_public_user(username):
    sql = "SELECT * from dir where username = '" + username + "';"
    return select_with_columns(sql)


def select_user_id(id):
    sql = "SELECT * from users where id = '" + str(id) + "';"
    return select(sql)

# def add_user_wallet(address, username):
#     sql = "UPDATE dir set address = '" + address + "' WHERE username = '" + username = "';" 
#     return select(sql)

def select_all_items():
    sql = "SELECT * from items;"
    return select_with_columns_item(sql)


def select_single_item(uuid):
    sql = "SELECT * from items where uuid ='" + uuid + "';"
    return select_with_columns_item(sql)


def select_user_items(username):
    sql = "SELECT * from items where owner = '" + username + "';"
    return select_with_columns_item(sql)


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

def insert_item(columns, r):
    try: 
        conn = psycopg2.connect(connection)
        cur = conn.cursor()
        q = 'insert into items (%s) values %s'
        exe = cur.mogrify(q, (
            AsIs(','.join(columns)),
            tuple([r[column] for column in columns])
        ))
        print(exe)
        cur.execute(exe)
        conn.commit()
        cur.close()
        conn.close()
        return {"success": True, "message": "data inserted successfully" }
    except Exception as e:
        print(e)
        return {"success": False, "message": str(e)}


def insert_hist(columns, r):
    try: 
        conn = psycopg2.connect(connection)
        cur = conn.cursor()
        q = 'insert into hist (%s) values %s returning uuid;'
        exe = cur.mogrify(q, (
            AsIs(','.join(columns)),
            tuple([r[column] for column in columns])
        ))
        print(exe)
        cur.execute(exe)
        conn.commit()
        data = cur.fetchone()
        cur.close()
        conn.close()
        return {"success": True, "message": data[0] }
    except Exception as e:
        print(e)
        return {"success": False, "message": str(e)}


def insert_fufillment(columns, r):
    try: 
        conn = psycopg2.connect(connection)
        cur = conn.cursor()
        q = 'insert into fufillment (%s) values %s'
        exe = cur.mogrify(q, (
            AsIs(','.join(columns)),
            tuple([r[column] for column in columns])
        ))
        print(exe)
        cur.execute(exe)
        conn.commit()
        cur.close()
        conn.close()
        return {"success": True, "message": data[0] }
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
        # wif = utils.create_wallet()
        # todo: sanitize this
            # add bsv wallet
        generate_user = '''insert into users (username, email, hash) values ('{}', '{}', '{}') ON CONFLICT DO NOTHING;
                        '''.format(username, email, generate_password_hash(password))

        generate_public = '''insert into dir (username) values ('{}')'''.format(username)

        r = insert(generate_user)
        r = insert(generate_public) # add user input possibility
        return r

    else:
        return {"success": False, "message": "Failed registration"}

