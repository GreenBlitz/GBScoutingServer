from app import server
from flask import render_template
from flask import request
import sqlite3


@server.route('/scouting', methods=['GET', 'POST'])
def add_data():
    # params = request.args
    # id = params.get('id')
    # password = params.get('password')
    try:
        conn = sqlite3.connect("Scouting_server_DB.db")
        curs = conn.cursor()
        # if password != curs.execute("SELECT psw FROM users WHERE id=?", (id)).fetchone():
        #     return #error code
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
            print(sql)
            curs.execute(sql)
            conn.commit()
            conn.close()
            return "Success"
    except sqlite3.Error as e:
        print(e)
        return "Error"
