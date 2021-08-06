from flask import request, jsonify
from app import server
import random
from app import PIN, ID, NAME, ROLE
import sqlite3


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
    global ID
    global NAME
    global ROLE
    global PIN

    ID += 1
    params = request.args
    pin = params.get('pin')
    psw = params.get('psw')

    if PIN != pin:
        return f'PIN was incorrect (Original PIN was {PIN}', 401

    data = ID, ROLE, NAME, psw

    conn = sqlite3.connect("db.db")
    curs = conn.cursor()
    curs.execute("""
            INSERT INTO users(id, name, role, psw)
            VALUES(?,?,?,?)                   
        """, data)

    conn.commit()
    conn.close()

    return jsonify(id=ID, name=NAME, role=ROLE)

