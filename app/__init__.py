PIN = 0

import sqlite3

conn_users = curs_users = None
conn_scouting_data = curs_scouting_data = None

try:
    conn_users = sqlite3.connect("test.db")
    curs_users = conn_users.cursor()
    curs_users.execute(""" CREATE TABLE IF NOT EXISTS  users(
                        id integer PRIMARY KEY,
                        name text,
                        role text,
                        PIN numeric (9,0),
                        pass text
                        );
                        """)

    conn_scouting_data = sqlite3.connect("scouting_data.db")
    curs_scouting_data = conn_users.cursor()
    curs_scouting_data.execute(""" CREATE TABLE IF NOT EXISTS  users(
                            timestamp time
                        );
                        """)


except sqlite3.Error as e:
    print(e)

from flask import Flask
server = Flask(__name__)


from app import views
from app import admin_views
from app import login_views