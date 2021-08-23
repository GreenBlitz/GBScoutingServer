from app import server
from app import game_rules
from flask import request, jsonify
import sqlite3


@server.route('/coach', methods=['GET'])
def get_team_data():
    params = request.args
    id = params.get('id')
    psw = params.get('psw')
    team_number = int(params.get('team'))

    conn = sqlite3.connect('Server.db')
    curs = conn.cursor()

    if psw != curs.execute("SELECT psw FROM users WHERE id=?", id).fetchone():
        return 'username or password does not exist', 401

    if 'coach' != curs.execute("SELECT role FROM users WHERE id=?", id).fetchone():
        return 'Access denied, you not the coach', 401

    select = ''
    for key in game_rules:
        select += game_rules[key][0] + ','

    select = select[:-1] + ' '

    team_data = curs.execute(f'SELECT {select} FROM team WHERE team={team_number}').fetchone()

    return team_data
