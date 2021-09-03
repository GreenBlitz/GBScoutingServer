from flask import request, jsonify
from app import server
import json
import requests
import datetime
import sqlite3

gmaeID_dictionary = {
    'qm': 'Qual',
    'qf': 'Quarter',
    'sf': 'Semi',
    'f': 'Final'
}


@server.route('/general/games', methods=['GET', 'POST'])
def games_page():
    params = json.loads(request.args.get('json').replace('%22', '"'))
    id = params["uid"]
    password = params["pass"]

    conn = sqlite3.connect("Server.db")
    curs = conn.cursor()
    # print(f'PASS {curs.execute("SELECT psw FROM users WHERE id=?", (id)).fetchone()[0]}')
    # print(f'PSW {password}')
    # if password != curs.execute("SELECT psw FROM users WHERE id=?", (id)).fetchone()[0]:
    #     return "username or password does not exist", 401

    url = 'https://www.thebluealliance.com/api/v3/event/2020isde1/matches/simple'

    headers = {'X-TBA-Auth-Key': 't6zONXbDuKDLpR6kXrId4Qluy0Gv8II95GgOzcHp8WHoxS5Gi68B3iKydHp3mfml'}

    j = requests.get(url, headers=headers).json()

    j = sorted(j, key=lambda k: k['actual_time'])

    games_page = []

    for game in j:
        timestamp = game['actual_time']
        time = str(datetime.datetime.fromtimestamp(timestamp))

        matchID = gmaeID_dictionary[game['comp_level']] + ' ' + str(game['match_number'])

        red_alliance = []
        for team in game['alliances']['red']['team_keys']:
            red_alliance.append(int(team[3:]))

        blue_alliance = []
        for team in game['alliances']['blue']['team_keys']:
            blue_alliance.append(int(team[3:]))

        alliances = [red_alliance, blue_alliance]

        games_page.append({'time': time,
                           'gameID': matchID,
                           'alliances': alliances
                           })
    ret = json.dumps({'games': games_page})
    print(f'GAMES PAGE RET : {ret}')
    return ret
