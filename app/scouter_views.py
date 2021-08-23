from app import server
from app import game_rules
from flask import render_template
from flask import request
import sqlite3


@server.route('/scouting', methods=['GET', 'POST'])
def add_data():
    params = request.args
    id = params.get('id')
    password = params.get('psw')
    try:
        conn = sqlite3.connect("Server.db")
        curs = conn.cursor()
        if password != curs.execute("SELECT psw FROM users WHERE id=?", id).fetchone():
            return "username or password does not exist", 401
        if request.method == 'POST':
            json = request.get_json()
            sql1 = "INSERT INTO team_game ("
            sql2 = ") VALUES ("
            for key in json.keys():
                sql1 += f"{key}, "
                sql2 += f"{json[key]}, "
            if sql1:
                sql1 = sql1[:-2]
                sql2 = sql2[:-2]
            sql = sql1 + sql2 + ');'
            curs.execute(sql)
            if not curs.execute(f"SELECT team FROM team WHERE team={json['team']}").fetchall():
                sql1 = "INSERT INTO team_game ("
                sql2 = ") VALUES ("
                for key in json.keys():
                    sql1 += f"{key}, "
                    sql2 += '0, '
                sql1 = sql1[:-2]
                sql2 = sql2[:-2]
                sql = sql1 + sql2 + ');'
                curs.execute(sql)
                conn.commit()
            for key in json.keys():
                if key == "team":
                    continue
                sql1 += f"{key}, "
                if game_rules[key][1] == "avg":
                    curr_avg = curs.execute(f"SELECT {key} FROM team WHERE team={json['team']}").fetchone()
                    num_of_games = curs.execute(f"SELECT num_of_games FROM team WHERE team=?", json["team"]).fetchone()
                    sum = curr_avg * num_of_games
                    new_avg = (sum + json[key])/(num_of_games+1)
                    sql = f"UPDATE team SET {key} = {new_avg}, num_of_games = {num_of_games+1} WHERE team={json['team']}"
                    curs.execute(sql)

                if game_rules[key][1] == "max":
                    curr = curs.execute(f"SELECT {key} FROM team WHERE team={json['team']}").fetchone()
                    num_of_games = curs.execute(f"SELECT num_of_games FROM team WHERE team=?", json["team"]).fetchone()
                    new_max = max(curr, json[key])
                    sql = f"UPDATE team SET {key} = {new_max}, num_of_games = {num_of_games+1} WHERE team={json['team']}"
                    curs.execute(sql)
            conn.commit()
            conn.close()
            return "Success"
    except sqlite3.Error as e:
        print(e)
        return "Error"

    return 'Sorry, for some reason we could not find what you searched for', 404
