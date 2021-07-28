import sqlite3
PIN = 0


def create_scouting_table(curs, values_data_types):
    sql = """ CREATE TABLE IF NOT EXISTS  (
                            id integer PRIMARY KEY,
                            timestamp time,
                            uname text,
                            game text,
                            team integer,

                        );
                        """
    for key in values_data_types.keys():
        sql += key + ' ' + values_data_types[key] + ','
    curs.execute(sql)


game_2020 = {
    "autonomous_balls": "integer",
    "cycles": "integer",
    "balls_per_cycle": "integer",
    "climbed?": "integer",
    "color_wheel": "integer"
}

conn = curs = None

try:
    conn = sqlite3.connect("Scouting_server_DB.db")
    curs = conn.cursor()
    curs.execute(""" CREATE TABLE IF NOT EXISTS  users(
                        id integer PRIMARY KEY,
                        name text,
                        role text,
                        psw text
                        );
                        """)

    create_scouting_table(curs, game_2020)


except sqlite3.Error as e:
    print(e)




from flask import Flask

server = Flask(__name__)

from app import views
from app import admin_views
from app import login_views
from app import scouter_views
