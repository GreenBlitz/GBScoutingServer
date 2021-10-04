
from app import server,  EVENT_KEY
from app import game_rules_2020
from flask import request, jsonify
import sqlite3
from json import loads, dumps
import re

from utils.tba_api import *


@server.route('/coach/team', methods=['GET'])
def get_team_data():
    params = loads(request.args.get('json').replace('%22', '"'))  #get params

    # auth
    id = params['id']
    psw = params['psw']
    team_number = params.get['team']

    conn = sqlite3.connect("Server.db")
    curs = conn.cursor()

    real_pass = curs.execute("SELECT psw FROM users WHERE id=?", (id,)).fetchone()
    if not real_pass:
        return f"user does not exist id = {id}", 401
    if psw != real_pass[0]:
        return 'password is incorrect', 401

    if 'coach' != curs.execute("SELECT role FROM users WHERE id=?", (id,)).fetchone()[0]:
        return 'Access denied, you not the coach', 403

    # read data
    select = ''
    for key in game_rules_2020.keys():
        select += f'AVG({key}),'
    select = select[:-1]

    team_data = curs.execute(f"SELECT {select} FROM team_game WHERE team=?", (team_number, )).fetchall()  # TODO add condition for game range
    if not team_data:
        return 'How do u want to get data before any game scoured, go shout at ur scouters', 503
    team_data = team_data[0]
    data_dict = dict(zip(game_rules_2020.keys(), team_data))

    # tba api data
    rank = get_rank(EVENT_KEY, str(team_number))
    alliance = get_alliance(EVENT_KEY, str(team_number))

    if not alliance:
        data_dict['ranking_or_alliance'] = str(rank)
    else:
        data_dict['ranking_or_alliance'] = alliance['name']

    win_rate = get_wins(EVENT_KEY, str(team_number))
    data_dict['win_rate'] = win_rate * 100

    data_dict['games'] = ['qual1', 'qual2', 'final1']

    json_data = dumps(data_dict)
    return json_data, 200
