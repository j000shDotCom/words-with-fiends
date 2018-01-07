"""
 Simple bot to log into and play WWF
"""
from requests import Session
from requests.auth import AuthBase


# TODO do something with this
class WWFAuth(AuthBase):
    def __init__(self, login, password):
        self.login = login
        self.password = password

    def __call__(self, r):

        # do something with the request here
        return r


def login():
    s = Session()

    querystring = {
        'bundle_name': 'WordsWithFriends3',
        'device_model': 'iPhone',
        'hash': hash_param,
        'zpid': zpid,
        'client_version': '10.26'
    }
    data = {
        'login_request': {'login': login, 'password': password}
    }
    headers = {
        'user-agent': 'WordsWithFriends3/10.26',
        'zpid': zpid,
        'zdid': zdid,
        'wfpw': wfpw
    }

    host = 'https://wordswithfriends.zyngawithfriends.com'
    s.get(host + '/jumps/config', params=querystring)

    url = '/sessions/create'
    s.post(host + url, json=data, headers=headers, params=querystring)

    return s


# not necessary - endpoint only exists to track behavior
# all user states remain active
def logout(s):
    # s.post('https://api.branch.io/v1/logout')
    pass


def get_games(s):
    pass


def get_letters(s, game):
    pass


def get_board_state(s, game):
    pass


def get_next_move(letters, state):
    pass


def make_move(s, move):
    pass


def main():
    s = login()
    games = get_games(s)
    for game in games:
        letters = get_letters(s, game)
        state = get_board_state(s, game)
        move = get_next_move(letters, state)
        make_move(s, move)


def get_daily_reward():
    s = login()
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
