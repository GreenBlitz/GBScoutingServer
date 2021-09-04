from app import server, DB_PATH, EVENT_KEY
from app import game_rules_2020
from flask import request, jsonify
import sqlite3
from json import loads, dumps
import re

from utils.tba_api import *


@server.route('/coach/team', methods=['GET'])
def get_team_data():
    params = loads(request.args.get('json').replace('%22', '"'))
    print("OREL:", params)
    id = params.get('id')
    psw = params.get('psw')
    team_number = params.get('team')

    conn = sqlite3.connect(DB_PATH)
    curs = conn.cursor()

    if psw != curs.execute("SELECT psw FROM users WHERE id=?", (id,)).fetchone()[0]:
        print('COACH ERROR: username or password does not exist')
        return 'username or password does not exist', 401

    if 'coach' != curs.execute("SELECT role FROM users WHERE id=?", (id,)).fetchone()[0]:
        print('COACH ERROR: Access denied, you not the coach')
        return 'Access denied, you not the coach', 401

    select = ''
    categories = re.compile("([a-zA-Z_0-9]+) ")
    for key in game_rules_2020.keys():
        select += f'{game_rules_2020[key].overview_types(key)},'

    team_data = \
        curs.execute(f'SELECT {", ".join(categories.findall(select))} FROM team WHERE team={team_number}').fetchall()[0]

    if not team_data:
        return 'How do u want to get data before any game scoured, go shout at ur scouters', 503

    data_dict = dict(zip(categories.findall(select), team_data))
    data_dict['comments'] = ''

    rank = get_rank(EVENT_KEY, str(team_number))
    alliance = get_alliance(EVENT_KEY, str(team_number))

    if not alliance:
        data_dict['ranking_or_alliance'] = str(rank)
    else:
        data_dict['ranking_or_alliance'] = alliance['name']

    win_rate = get_wins(EVENT_KEY, str(team_number))

    data_dict['win_rate'] = win_rate * 100

    data_dict['color_wheel_1_avg'] *= 100
    data_dict['color_wheel_2_avg'] *= 100
    data_dict['climb_avg'] *= 100

    data_dict['games'] = ['qual1', 'qual2', 'final1']

    json_data = dumps(data_dict)
    print(f'ASAFFFFFFFFF: {json_data}')
    return json_data
