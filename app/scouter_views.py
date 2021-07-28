from app import server
from flask import render_template
from flask import request
import sqlite3


@server.route('/scouting', methods=['GET', 'POST'])
def add_data():
    params = request.args
    id = params.get('id')
    password = params.get('password')
    try:
        conn = sqlite3.connect("Scouting_server_DB.db")
        curs = conn.cursor()
    except sqlite3.Error as e:
        print(e)
    if password != curs.execute("SELECT psw FROM users WHERE id=?", (id)).fetchone():
        return #error code
    if request.method == 'POST':
        json = request.form
        print(json)
        print(type(json))
