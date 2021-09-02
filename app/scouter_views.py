from app import server
from app import game_rules_2020
from flask import request
import sqlite3
import json


@server.route('/scouter/send', methods=['GET', 'POST'])
def add_data():
    params = json.loads(request.args.get('json').replace('%22', '"'))
    print(f"PARAMS: {params}  + {type(params)}")
    id = params["uid"]
    password = params["psw"]

    try:
        conn = sqlite3.connect("Server.db")
        curs = conn.cursor()
        if password != curs.execute("SELECT psw FROM users WHERE id=?", id).fetchone()[0]:
            return "username or password does not exist", 401
        if 'scouter' != curs.execute("SELECT role FROM users WHERE id=?", id).fetchone()[0]:
            return 'Access denied, you not the scouter', 401
        if request.method == 'POST':
            sql1 = f"INSERT INTO team_game (id, timestamp, username"
            sql2 = f") VALUES (?, ?, ?"
            data = [(curs.execute('SELECT MAX(id) from team_game').fetchone()[0] if curs.rowcount != 0 else 0) + 1, curs.execute("SELECT datetime('now', 'localtime')").fetchone()[0], curs.execute("SELECT name FROM users WHERE id=?", id).fetchone()[0]]
            for key in params.keys()[2:]:
                sql1 += f", {key}"
                sql2 += f", ?"
                data.append(params[key])
            sql = sql1 + sql2 + ');'
            curs.execute(sql, data)
            if not curs.execute(f"SELECT team FROM team WHERE team=?", params['team']).fetchall():
                sql1 = "INSERT INTO team_game (id, team"
                curs.execute("SELECT MAX(id) FROM team")
                sql2 = f") VALUES (?, ?"
                data =[(curs.fetchone()[0] if curs.rowcount != 0 else 0) + 1, params['team']]
                for name in list(map(lambda x: params[x].overview_types(x), game_rules_2020.keys())):
                    sql1 += f", {name}"
                    sql2 += ', ?'
                    data.append(0)
                sql = sql1 + sql2 + ');'
                curs.execute(sql, data)
                conn.commit()
            for key in params.keys()[2:]:
                if key == "team":
                    continue
                overview = game_rules_2020[key].recreate(key, curs, "team", f"team={params['team']}")
                overview.add(params["key"])
                curs.execute(f"UPDATE team SET ? = ?, ? = ?, ? = ? WHERE team={params['team']}", overview.split(key))
            conn.commit()
            conn.close()
            return "Success"
    except sqlite3.Error as e:
        print(e)
        return "Error"

    return 'Sorry, for some reason we could not find what you searched for', 404


