"""
 Simple bot to log into and play WWF
"""
from requests import Session
import json
from .user import User
from .move import Move
from .game import Game
from config import Config

class WWF(object):
    def __init__(self, login, password):
        self.s = Session()
        self.s.hooks['response'].append(_log_request_status)
        self.s.headers.update({'Accept': 'application/json'})


    def initialize(self):
        self.get_auth_token()
        self.get_initial_config()
        self.user = User(self.login(login, password))
        self.misc_user_data = self.get_user_data()


    def get_games(self):
        return [Game(g) for g in self.get_game_data()]

    def can_make_move(self, game):
        return game.can_make_move(self.user)

    def store_games(self, games):
        pass

    def store_words(self, words):
        pass

    ### REQUESTS ###
    def login_with_email(self, email, password):
        #url = 'https://http2.api.zynga.com/gwf/password'
        url = 'https://http2.api.zynga.com/gwf/sessions/create'
        params = {
            'bundle_name': 'WordsWithFriends3',
            'device_model': 'iPhone',
            'hash': '9ce926da851ea7652e23a44ddf064f6eee7fafe3',
            'zpid': '57A4F64E-DE57-4220-B002-1BCFEF210E2E',
            'client_version': 14.52
        }
        payload = {
            'login_request': {
                'login': email,
                'password': password
            }
        }
        r = self.s.post(url, params=params, json=payload)


    def get_auth_token(self):
        url = 'https://api.zynga.com/auth/issueToken'
        params = {
            'appId': '5003741',
            'password': 'sss',
            'userId': 'sss'
        }
        r = self.s.post(url, params=params)

    def get_initial_config(self):
        url = '/jumps/config'
        query = {
            'bundle_name': Config.BUNDLE_NAME,
            'client_version': Config.CLIENT_VERSION,
            'plaintext': 1,
        }
        r = self.s.get(Config.WWF_HOST + url, params=query)
        conf = json.loads(r.text)

        self.MAXACTIVE = int(conf['MaxActiveGamesForCreate'])
        self.BLACKLIST = conf['BlackListedWords'].split(',')
        self.WHITELIST = conf['WhiteListedWords'].split(',')

    def login_with_token(self, login, password):
        url = '/sessions/create'
        data = {
            'login_request': {'login': login, 'password': password}
        }
        r = self.s.post(Config.WWF_HOST + url, json=data)
        return json.loads(r.text)

    def get_user_data(self):
        url = '/user_data'
        params = {
            'badges': True,
            'game_type': 'WordGame',
            'include_item_data': True
        }
        r = self.s.get(Config.WWF_HOST + url, params=params)
        return json.loads(r.text)

    def get_game_data(self):
        url = '/games'
        params = {
            'game_type': 'WordGame',
            'get_current_user': True,
            'include_invitations': True,
            'include_item_data': True,
            'chat_messages_since': 0,
            'moves_since': 0
        }
        r = self.s.get(Config.WWF_HOST + url, params=params)
        return json.loads(r.text)['games']

    def make_move(self, move):
        url = '/moves'
        params = {
            'points': move.points,
            'words': move.words
        }
        data = {
            'move': move
        }
        r = self.s.post(Config.WWF_HOST + url, params=params, json=data)
        return json.loads(r.text)

    def get_chat_messages(self, user):
        pass

    def send_chat_message(self, user, mesg):
        pass

    def get_daily_drip(self):
        url = '/packages/grant_daily_drip'
        return self.s.get(Config.WWF_HOST + url)

### HELPER METHODS ###
def _log_request_status(r, *args, **kwargs):
    parts = [r.status_code, r.request.method, r.request.url]
    if r.request.body:
        parts.append(r.request.body)
    print(*parts)

    if not r.ok:
        parts.append(r.text)
        raise ValueError('Request Failed: ', *parts)
