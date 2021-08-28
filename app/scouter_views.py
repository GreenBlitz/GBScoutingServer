from app import server
from app import game_rules
from flask import render_template
from flask import request
import sqlite3


@server.route('/scouter/send', methods=['GET', 'POST'])
def add_data():
    params = request.args
    print("PARAMS: " + params.__str__())
    id = params.get('id')
    password = params.get('psw')
    try:
        conn = sqlite3.connect("Server.db")
        curs = conn.cursor()
        if password != curs.execute("SELECT psw FROM users WHERE id=?", id).fetchone()[0]:
            return "username or password does not exist", 401
        if 'scouter' != curs.execute("SELECT role FROM users WHERE id=?", id).fetchone()[0]:
            return 'Access denied, you not the scouter', 401
        if request.method == 'POST':
            json = request.get_json()
            sql1 = f"INSERT INTO team_game (id, "
            curs.execute('SELECT MAX(id) from team_game')
            sql2 = f") VALUES ({(curs.fetchone()[0] if curs.rowcount != 0 else 0) + 1}, "
            for key in json.keys():
                sql1 += f"{key}, "
                sql2 += f"{json[key]}, "
            if sql1:
                sql1 = sql1[:-2]
                sql2 = sql2[:-2]
            sql = sql1 + sql2 + ');'
            curs.execute(sql)
            if not curs.execute(f"SELECT team FROM team WHERE team={json['team']}").fetchall():
                sql1 = "INSERT INTO team_game (id, "
                curs.execute("SELECT MAX(id) FROM team")
                sql2 = f") VALUES ({(curs.fetchone()[0] if curs.rowcount != 0 else 0) + 1}, "
                for key in json.keys():
                    sql1 += f"{game_rules[key][1].sql_types(key)}, "
                    sql2 += '0, '
                sql1 = sql1[:-2]
                sql2 = sql2[:-2]
                sql = sql1 + sql2 + ');'
                curs.execute(sql)
                conn.commit()
            for key in json.keys():
                if key == "team":
                    continue
                curs.execute("SELECT ?_")
                #sql = f"UPDATE team SET ? = ?, num_of_games = {num_of_games+1} WHERE team={json['team']}"
                curs.execute(sql, (key, new_avg))
            conn.commit()
            conn.close()
            return "Success"
    except sqlite3.Error as e:
        print(e)
        return "Error"

    return 'Sorry, for some reason we could not find what you searched for', 404
