from flask import request, jsonify
from app import server
import random
from app import PIN, NAME, ROLE
import sqlite3
import json

MASTER_PASS_HASHED = "8c8f7c9c5b2194fb60ac6f8847bfe9145a67a006245f39ee8a8901ae776f98f0"


@server.route('/auth/add', methods=['GET', 'POST'])
def register_user():
    global PIN
    global NAME
    global ROLE

    params = request.args
    NAME = params.get('uname')
    ROLE = params.get('role')

    PIN = str(random.randint(10000, 99999))
    print(PIN)
    return fr"{NAME} the {ROLE}'s PIN is: {PIN}"


@server.route('/auth/register', methods=['GET', 'POST'])
def register_from_device():
    global NAME
    global ROLE
    global PIN

    params = json.loads(request.args.get('json').replace('%22', '"'))
    print(params)
    pin = params['PIN']
    psw = params['pass']

    print(f'PIN {PIN}, pin {pin}')

    if PIN != pin:
        return f'PIN was incorrect (Original PIN was {PIN}', 401

    conn = sqlite3.connect("Server.db")
    curs = conn.cursor()
    curs.execute('SELECT MAX(id) from users')

    data = curs.fetchone()

    print(f'DATA: {data}')

    ID = (data[0] + 1 if data[0] else 1)
    data = ID, NAME, ROLE, psw
    print('(id role name psw ) ', data)
    curs.execute("""
            INSERT INTO users(id, name, role, psw)
            VALUES(?,?,?,?)                   
        """, data)

    conn.commit()
    conn.close()

    return jsonify(uid=ID, name=NAME, role=ROLE)
