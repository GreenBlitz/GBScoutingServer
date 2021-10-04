from flask import request, jsonify
from app import server, EVENT_KEY
import json
import requests
import datetime
import sqlite3

from utils.tba_api import get_games

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

    games = get_games(EVENT_KEY)
    if games[0] == -1:
        return "error from tba api", 502
    sort = sorted(games, key=lambda k: k['actual_time'])

    games_page = []

    for game in sort:
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
    return ret, 200
