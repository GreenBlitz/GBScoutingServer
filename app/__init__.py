import sqlite3


PIN = ''
NAME = ''
ROLE = ''
ID = 0


EVENT_KEY = '2019isde1'

game_rules_2020 = {
    "auto_balls": "INTEGER",  # numeric
    "tele_balls": "INTEGER",
    "cycles": "INTEGER",

    "color_wheel_1": "INTEGER",  # boolean expressed as 0 or 1
    "color_wheel_2": "INTEGER",
    "climb": "INTEGER"
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

    sql = """ CREATE TABLE if not exists team_game(
                id integer PRIMARY KEY,
                timestamp datetime,
                username text,
                game text,
                team integer,
                comments text"""

    for key in game_rules_2020.keys():
        # print("game rules: ", game_rules_2020[key])
        # print("game rules type: ", game_rules_2020[key].this_type(key), "\n")
        sql += ',\n' + key +" " +  game_rules_2020[key]
    sql += ');'
    curs.execute(sql)

    conn.close()

except sqlite3.Error as e:
    print(e)



from flask import Flask

server = Flask(__name__)
server.config['ENV'] = 'development'
# server.config['TESTING'] = True

from app import views
from app import admin_views
from app import auth_views
from app import scouter_views
from app import coach_views
from app import general_views