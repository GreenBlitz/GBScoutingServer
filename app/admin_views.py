from app import server
from hashlib import sha256
from flask import request
import sqlite3


@server.route('/admin')
def admin():
    return 'GBAdmin'  # render_template('admin/admin.html')


@server.route('/self/destruct/button')
def self_destruct():
    psw = sha256(request.args.get('sequence').encode()).hexdigest()
    if psw == '7577076447538d8a36c165212eefe9384740321914889fbe7e760cebf06199ab':
        conn = sqlite3.connect('Server.db')
        curs = conn.cursor()
        curs.execute('DELETE FROM users')
        curs.execute('DELETE FROM team_game')
        curs.execute('DELETE FROM team')
        conn.commit()

    return "I'm a teapot", 418
