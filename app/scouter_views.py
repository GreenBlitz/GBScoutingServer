from app import server
from app import game_rules_2020, DB_PATH
from flask import request
import sqlite3
import json
import re


@server.route('/scouter/send', methods=['GET', 'POST'])
def add_data():
    params = json.loads(request.args.get('json').replace('%22', '"'))
    id = params["uid"]
    password = params["psw"]
    team_number = params['team']

    del params['uid']
    del params['psw']

    conn = sqlite3.connect(DB_PATH)
    curs = conn.cursor()
    if password != curs.execute("SELECT psw FROM users WHERE id=?", (id,)).fetchone()[0]:
        return "username or password does not exist", 401
    if 'scouter' != curs.execute("SELECT role FROM users WHERE id=?", (id,)).fetchone()[0]:
        return 'Access denied, you not the scouter', 401
    if request.method == 'POST':
        sql1 = f"INSERT INTO team_game (id, timestamp, username"
        sql2 = f") VALUES (?, ?, ?"

        current_data = curs.execute('SELECT MAX(id) from team_game').fetchone()[0]
        data = [(current_data if current_data else 0) + 1,
                curs.execute("SELECT datetime('now', 'localtime')").fetchone()[0],
                curs.execute("SELECT name FROM users WHERE id=?", (id,)).fetchone()[0]]
        for key in list(params.keys())[:2]:
            sql1 += f", {key}"
            sql2 += f", ?"
            data.append(params[key])
        sql = sql1 + sql2 + ');'
        curs.execute(sql, data)
        if not curs.execute(f"SELECT team FROM team WHERE team=?", (team_number,)).fetchall():
            sql1 = "INSERT INTO team_game (id, team"
            sql2 = f") VALUES (?, ?"
            current_data = curs.execute("SELECT MAX(id) FROM team").fetchone()[0]
            data = [10, team_number]  # [(current_data if current_data else 0) + 1, team_number]
            for name in list(params.keys()):
                sql1 += f", {name}"
                sql2 += ', ?'
                data.append(0)
            sql = sql1 + sql2 + ');'


            curs.execute(sql, tuple(data))
            conn.commit()

        print('PARAMS:', params)
        for key in list(params.keys()):
            if key == "team" or "comments":
                continue
            overview = game_rules_2020[key].recreate(key, curs, "team", f"team={team_number}")
            thing = params[key]
            overview.add(thing)
            print('ASAFFFFFF',  overview.split(key))


            asaf = overview.split(key)
            print('sql', f"UPDATE team SET {asaf[0]} = {asaf[1]}, {asaf[2]} = {asaf[3]}, {asaf[4]} = {asaf[5]} WHERE team={params['team']}", overview.split(key))

            curs.execute(f"UPDATE team SET {asaf[0]} = {asaf[1]}, {asaf[2]} = {asaf[3]}, {asaf[4]} = {asaf[5]} WHERE team={params['team']}")
        conn.commit()
        conn.close()
        return "Success"
