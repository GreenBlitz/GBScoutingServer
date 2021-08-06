import sqlite3
ID = 0
PIN = ''
NAME = ''
ROLE = ''


game_rules = {
    "autonomous_balls": ("integer", "avg"),
    "cycles": ("integer", "avg"),
    "balls_per_cycle": ("", "avg"),
    "climbed": ("integer", "max"),
    "color_wheel": ("integer", "max")
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
                timestamp time,
                username text,
                game text,
                team integer"""

    for key in game_rules.keys():
        sql += ',\n' + key + ' ' + game_rules[key][0]
    sql += ');'
    curs.execute(sql)
    sql = """ CREATE TABLE if not exists team(
                id integer PRIMARY KEY,
                team integer
                num_of_games integer"""

    for key in game_rules.keys():
        sql += ',\n' + key + ' ' + game_rules[key][0]
    sql += ');'
    curs.execute(sql)

    conn.close()

except sqlite3.Error as e:
    print(e)




from flask import Flask

server = Flask(__name__)

from app import views
from app import admin_views
from app import auth_views
from app import scouter_views
