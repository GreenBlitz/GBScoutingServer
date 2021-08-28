from app import server
from app import game_rules_2020
from flask import request, jsonify
import sqlite3


@server.route('/coach/team', methods=['GET'])
def get_team_data():
    params = request.args
    id = params.get('id')
    psw = params.get('psw')
    team_number = int(params.get('team'))

    conn = sqlite3.connect('Server.db')
    curs = conn.cursor()

    if psw != curs.execute("SELECT psw FROM users WHERE id=?", id).fetchone()[0]:
        return 'username or password does not exist', 401

    if 'coach' != curs.execute("SELECT role FROM users WHERE id=?", id).fetchone()[0]:
        return 'Access denied, you not the coach', 401

    select = ''
    for key in game_rules.keys():
        select += f'{key},'

    select = select[:-1] + ' '

    team_data = curs.execute(f'SELECT {select} FROM team WHERE team={team_number}').fetchone()
    if team_data == None:
        return 'How do u want to get data before any game scoured, go shout on ur scouters', 503

    return jsonify(dict(zip(game_rules.keys(), team_data)))
