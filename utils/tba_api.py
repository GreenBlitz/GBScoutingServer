import requests
auth = "nsydEycbcbK5YX4RK2eV9uoOBiFpkcivKdYlfFF0my3M6E9AvAqyB5ByrrQlYTjG"


def get_team_status(event_key, team_number):
    return requests.get(f"https://thebluealliance.com/api/v3/event/{event_key}/teams/statuses", headers={"X-TBA-Auth-Key" : auth}).json()["frc" + team_number]


def get_wins(event_key, team):
    l_t_w = get_team_status(event_key, team)['qual']['ranking']['record']
    l = l_t_w['losses']
    t = l_t_w['ties']
    w = l_t_w['wins']
    return (w + 0.5*t)/(w + t + l)



def get_alliance(event_key, team):
    return get_team_status(event_key, team)['alliance']

def get_rank(event_key, team):
    return get_team_status(event_key, team)['qual']['ranking']['rank']