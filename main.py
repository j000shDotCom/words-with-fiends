"""
 Simple bot to log into and play WWF
"""
from requests import Session
import json


HOST = 'https://wordswithfriends.zyngawithfriends.com'
BUNDLE_NAME = 'WordsWithFriends3'
CLIENT_VERSION = '10.26'


def _log_request_status(r, *args, **kwargs):
    parts = [r.status_code, r.request.method, r.request.url]
    if r.request.body:
        parts.append(r.request.body)
    print(*parts)

    if not r.ok:
        parts.append(r.text)
        raise ValueError('Request Failed: ', *parts)


def login(login, password):
    s = Session()

    s.hooks['response'].append(_log_request_status)

    url = '/jumps/config'
    query = {
        'bundle_name': BUNDLE_NAME,
        'client_version': CLIENT_VERSION
    }
    s.get(HOST + url, params=query)

    url = '/sessions/create'
    data = {
        'login_request': {'login': login, 'password': password}
    }
    s.post(HOST + url, json=data)
    return s


def get_user_data(s):
    url = '/user_data'
    params = {
        'badges': True,
        'game_type': 'WordGame',
        'include_item_data': True
    }
    r = s.get(HOST + url, params=params)
    d = json.loads(r.text)


def get_games(s):
    url = '/games'
    params = {
        'game_type': 'WordGame',
        'get_current_user': True,
        'include_invitations': True,
        'include_item_data': True
    }
    headers = {
        'Content-Type': 'application/json'
    }
    r = s.get(HOST + url, params=params, headers=headers)
    d = json.loads(r.text)


def get_letters(s, game):
    pass


def get_board_state(s, game):
    pass


def get_next_move(letters, state):
    pass


def make_move(s, move):
    pass


def get_chat_messages(s, user):
    pass


def main():
    s = login(username, password)
    data = get_user_data(s)
    games = get_games(s)
    for game in games:
        letters = get_letters(s, game)
        state = get_board_state(s, game)
        move = get_next_move(letters, state)
        make_move(s, move)


def get_daily_reward():
    s = login(username, password)
    url = '/packages/grant_daily_drip'
    s.get(HOST + url)


""" TODO
- get games
- for each game
  - get letters
  - get board state
  - make valid move
- get challenges
- for each challenge
  - get letters
  - get board state
  - make valid move
"""

main()
