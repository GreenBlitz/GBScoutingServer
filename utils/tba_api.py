import requests

auth = "nsydEycbcbK5YX4RK2eV9uoOBiFpkcivKdYlfFF0my3M6E9AvAqyB5ByrrQlYTjG"

comp_level = {"qm": 1,
              'qf': 2,
              'sf': 3,
              'f': 4}


def get_team_status(event_key, team_number):
    answer = requests.get(f"https://thebluealliance.com/api/v3/event/{event_key}/teams/statuses",
                          headers={"X-TBA-Auth-Key": auth})
    if answer.status_code // 100 != 2:
        print(f"error in get team status from tba api, error: {answer.status_code}")
        return -1
    return answer.json()["frc" + team_number]


def get_wins(event_key, team):
    status = get_team_status(event_key, team)
    if status == -1:
        return 0
    l_t_w = status['qual']['ranking']['record']
    l = l_t_w['losses']
    t = l_t_w['ties']
    w = l_t_w['wins']
    return (w + 0.5 * t) / (w + t + l)


def get_alliance(event_key, team):
    return get_team_status(event_key, team)['alliance']


def get_rank(event_key, team):
    return get_team_status(event_key, team)['qual']['ranking']['rank']


def get_games(event_key):
    url = f'https://www.thebluealliance.com/api/v3/event/{event_key}/matches/simple'

    headers = {'X-TBA-Auth-Key': auth}

    answer = requests.get(url, headers=headers)
    if answer.status_code // 100 != 2:
        print(f"error in get games from tba api, error: {answer.status_code}")
        return -1
    return answer.json()


def get_one_game(game_key):
    url = f'https://www.thebluealliance.com/api/v3/match/{game_key}/simple'

    headers = {'X-TBA-Auth-Key': auth}

    answer = requests.get(url, headers=headers)
    if answer.status_code // 100 != 2:
        print(f"error in get games from tba api, error: {answer.status_code}")
        return -1
    return answer.json()


def are_games_after(min_game, games):
    min_game = get_one_game(min_game)
    filtered_games = filter(
        lambda i: comp_level[i['comp_level']] * 10000 + min_game['match_number'] > comp_level[i['comp_level']] * 10000 +
                  min_game['match_number'], games)
    return filtered_games


if __name__ == '__main__':
    print(get_games("2019iscmp"))
