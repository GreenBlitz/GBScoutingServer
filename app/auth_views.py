from flask import request, jsonify
from app import server
import random
from app import PIN, NAME, ROLE
import sqlite3
import json

MASTER_PASS_HASHED = "8c8f7c9c5b2194fb60ac6f8847bfe9145a67a006245f39ee8a8901ae776f98f0"


@server.route('/auth/add', methods=['GET', 'POST'])
def add():
    global PIN
    global NAME
    global ROLE

    params = request.args
    NAME = params.get('uname')
    ROLE = params.get('role')

    if not NAME or not ROLE:
        return "please enter name and role of new user", 401

    PIN = str(random.randint(10000, 99999))
    return fr"{NAME} the {ROLE}'s PIN is: {PIN}", 200


@server.route('/auth/register', methods=['GET', 'POST'])
def register():
    global NAME
    global ROLE
    global PIN

    params = json.loads(request.args.get('json').replace('%22', '"'))

    pin = params['PIN']  # pin is string
    psw = params['pass']

    if PIN != pin:
        return f'PIN was incorrect (Original PIN was {PIN}', 401
    if not psw:
        return "please set a psw for user", 401

    conn = sqlite3.connect("Server.db")
    curs = conn.cursor()
    curs.execute('SELECT MAX(id) from users')

    data = curs.fetchone()

    ID = (data[0] + 1 if data[0] else 1)
    data = ID, NAME, ROLE, psw
    curs.execute("""
            INSERT INTO users(id, name, role, psw)
            VALUES(?,?,?,?)                   
        """, data)

    conn.commit()
    conn.close()

    return jsonify(uid=ID, name=NAME, role=ROLE), 200


@server.route('/auth/login', methods=['GET', 'POST'])
def login():
    params = json.loads(request.args.get('json').replace('%22', '"'))
    uid = params['uid']
    psw = params['pass']

    conn = sqlite3.connect('Server.db')
    curs = conn.cursor()

    real_pass = curs.execute("SELECT psw FROM users WHERE id=?", (uid,)).fetchone()
    if not real_pass:
        return json.dumps({'name': None, 'role': None, 'success': False}), 401
    if psw != real_pass[0]:
        return json.dumps({'name': None, 'role': None, 'success': False}), 503

    data = (uid, psw)

    name, role = curs.execute("SELECT name, role FROM users WHERE id=? AND psw=?", data).fetchall()[0]

    return json.dumps({'name': name, 'role': role, 'success': True}), 200
