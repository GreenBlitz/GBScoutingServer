ID = 0
PIN = ''
NAME = ''
ROLE = ''

import sqlite3

conn = curs = None

try:
    conn = sqlite3.connect("db.db")
    curs = conn.cursor()
    curs.execute(""" CREATE TABLE IF NOT EXISTS  users(
                        id integer PRIMARY KEY,
                        name text,
                        role text,
                        psw text
                        );
                        """)

    curs.execute(""" CREATE TABLE IF NOT EXISTS  scouting(
                            timestamp time
                        );
                        """)

    conn.close()

except sqlite3.Error as e:
    print(e)

from flask import Flask
server = Flask(__name__)


from app import views
from app import admin_views
from app import auth_views