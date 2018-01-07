"""
 Simple bot to log into and play WWF
"""
from requests import Session


def login(login, password):
    s = Session()

    host = 'https://wordswithfriends.zyngawithfriends.com'

    url = '/jumps/config'
    query = {
        'bundle_name': 'WordsWithFriends3',
        'client_version': '10.26'
    }
    s.get(host + url, params=query)

    url = '/sessions/create'
    data = {
        'login_request': {'login': login, 'password': password}
    }
    s.post(host + url, json=data)
    return s


def get_games(s):
    return []


def get_letters(s, game):
    pass


def get_board_state(s, game):
    pass


def get_next_move(letters, state):
    pass


def make_move(s, move):
    pass


def main():
    s = login(username, password)
    games = get_games(s)
    for game in games:
        letters = get_letters(s, game)
        state = get_board_state(s, game)
        move = get_next_move(letters, state)
        make_move(s, move)


def get_daily_reward():
    s = login(username, password)

    host = 'https://wordswithfriends.zyngawithfriends.com'
    url = '/packages/grant_daily_drip'
    headers = {
        '': ''
    }
    s.get(host + url, headers=headers)


""" TODO
1 get games
2 get laetters
3 get board state
4 make valid move
"""

main()
