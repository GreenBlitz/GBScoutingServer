from app import server
from app import game_rules_2020
from flask import request
import sqlite3
import json
import re


@server.route('/scouter/send', methods=['GET', 'POST'])
def add_data():
    # auth
    params = json.loads(request.args.get('json').replace('%22', '"'))
    id = params["uid"]
    password = params["psw"]

    del params['uid']
    del params['psw']

    conn = sqlite3.connect("Server.db")
    curs = conn.cursor()
    real_pass = curs.execute("SELECT psw FROM users WHERE id=?", (id,)).fetchone()
    if not real_pass:
        return f"user does not exist id = {id}", 401
    if password != real_pass[0]:
        return "password is incorrect", 401
    if 'scouter' != curs.execute("SELECT role FROM users WHERE id=?", (id,)).fetchone()[0]:
        return 'Access denied, you not the scouter', 401

    # update sql
    if request.method == 'POST':
        # sql1 = f"INSERT INTO team_game (id, timestamp, username"
        # sql2 = f") VALUES (?, ?, ?"
        #
        # current_data_01 = curs.execute('SELECT MAX(id) from team_game').fetchone()
        # current_data = current_data_01[0]
        # print('Cur rent Data', current_data_01)
        # data = [(current_data if current_data else 0) + 1,
        #         curs.execute("SELECT datetime('now', 'localtime')").fetchone()[0],
        #         curs.execute("SELECT name FROM users WHERE id=?", (id,)).fetchone()[0]]
        # for key in list(params.keys())[:2]:
        #     sql1 += f", {key}"
        #     sql2 += f", ?"
        #     data.append(params[key])
        # sql = sql1 + sql2 + ');'
        #
        # print('SQL + DATA 1 :', sql, data)

        # curs.execute(sql, data)

        sql1 = "INSERT INTO team_game (id,  username"
        sql2 = f") VALUES (?, ?, ?"
        current_data = curs.execute("SELECT MAX(id) FROM team_game").fetchone()[0]
        data = [(current_data + 1 if current_data else 1),

                curs.execute("SELECT name FROM users WHERE id=?", (id,)).fetchone()[0]]
        for key in list(params.keys()):
            sql1 += f", {key}"
            sql2 += f", ?"
            data.append(params[key])
        sql = sql1 + sql2 + ');'

        curs.execute(sql, data)
        conn.commit()
        conn.close()
        return "Success", 200
    else:
        return "request must be post", 400
