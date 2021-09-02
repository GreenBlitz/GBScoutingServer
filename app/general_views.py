from flask import request, jsonify
from app import server
import json


@server.route('/general/games', methods=['GET', 'POST'])
def games_page():
    params = json.loads(request.args.get('json').replace('%22', '"'))
    print(f"PARAMS: {params}  + {type(params)}")
    id = params["uid"]
    password = params["pass"]

    g1 = {"time": "12:00",
          "gameID": "qual1",
          "teams": [['red1', 'red2', 'red3'], ['blue1', 'blue2', 'blue3']]
          }
    g2 = {"time": "12:10",
          "gameID": "qual2",
          "teams": [['red1', 'red2', 'red3'], ['blue1', 'blue2', 'blue3']]
          }
    g3 = {"time": "12:20",
          "gameID": "qual3",
          "teams": [['red1', 'red2', 'red3'], ['blue1', 'blue2', 'blue3']]
          }

    games = [g1, g2, g3]

    return json.dumps({"games": games})

