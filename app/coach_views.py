from app import server
from app import game_rules_2020
from flask import request, jsonify
import sqlite3
from json import loads
import re

@server.route('/coach/team', methods=['GET'])
def get_team_data():
    params = loads(request.args.get('json').replace('%22', '"'))
    print("OREL:", params)
    id = params.get('id')
    psw = params.get('psw')
    team_number = int(params.get('team'))

    conn = sqlite3.connect('Server.db')
    curs = conn.cursor()

    if psw != curs.execute("SELECT psw FROM users WHERE id=?", (id,)).fetchone()[0]:
        return 'username or password does not exist', 401

    if 'coach' != curs.execute("SELECT role FROM users WHERE id=?", (id,)).fetchone()[0]:
        return 'Access denied, you not the coach', 401

    select = ''
    categories = re.compile("([a-zA-Z_0-9]+) ")
    for key in game_rules_2020.keys():
        select += f'{game_rules_2020[key].overview_types(key)},'

    # select = ", ".join(categories.findall(select))

    print("NIGGA:", categories.findall(select)[0])
    print("NIGGGA:", curs.execute(f'SELECT {categories.findall(select)[0]} FROM team').fetchall())
    team_data = curs.execute(f'SELECT {list(categories.finditer(select))[0]} FROM team WHERE team={team_number}')
    print(team_data.fetchall())
    team_data = team_data.fetchone()[0]
    if team_data == None:
        return 'How do u want to get data before any game scoured, go shout on ur scouters', 503

    json = jsonify(dict(zip(game_rules_2020.keys(), team_data)))
    print(json)
    return json
