
ID = 0
PIN = ''
NAME = ''
ROLE = ''
import sqlite3




def create_scouting_table(values_data_types):
    sql = """ CREATE TABLE if not exists team_game(
                id integer PRIMARY KEY,
                timestamp time,
                username text,
                game text,
                team integer"""

    for key in values_data_types.keys():
        sql += ',\n' + key + ' ' + values_data_types[key]
    sql += ');'
    return sql


game_2020 = {
    "autonomous_balls": "integer",
    "cycles": "integer",
    "balls_per_cycle": "integer",
    "climbed": "integer",
    "color_wheel": "integer"
}

conn = curs = None

try:
    conn = sqlite3.connect("Server.db")
    curs = conn.cursor()
    curs.execute(""" CREATE TABLE if not exists users(
                        id integer PRIMARY KEY,
                        name text,
                        role text,
                        psw text
                        );
                        """)
    curs.execute(create_scouting_table(game_2020))
    conn.close()

except sqlite3.Error as e:
    print(e)




from flask import Flask

server = Flask(__name__)

from app import views
from app import admin_views
from app import auth_views
from app import scouter_views
