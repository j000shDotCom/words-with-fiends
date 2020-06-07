import json

from requests import Session
from ..config import Config
from ..helpers import _log_request_status, _wrap_response

class WwfClient():
    def __init__(self, login, password):
        self.s = Session()
        self.s.hooks['response'].append(_log_request_status)
        self.s.headers.update({'Accept': 'application/json'})


    def login_with_email(self, email, password):
        #url = 'https://http2.api.zynga.com/gwf/password'
        url = Config.WWF_HTTP2_HOST + '/gwf/sessions/create'
        params = {
            'bundle_name': Config.BUNDLE_NAME,
            'device_model': Config.DEVICE_MODEL,
            # 'hash': '9ce926da851ea7652e23a44ddf064f6eee7fafe3',
            # 'zpid': '57A4F64E-DE57-4220-B002-1BCFEF210E2E',
            'client_version': Config.CLIENT_VERSION
        }
        payload = {
            'login_request': {
                'login': email,
                'password': password
            }
        }
        r = self.s.post(url, params=params, json=payload)
        return json.loads(r.text)


    def get_auth_token(self):
        url = Config.WWF_ZYNGA_HOST + '/auth/issueToken'
        params = {
            'appId': Config.WWF_APP_ID,
            'password': 'sss',
            'userId': 'sss'
        }
        r = self.s.post(url, params=params)


    def login_with_token(self, login, password):
        url = '/sessions/create'
        data = {
            'login_request': {'login': login, 'password': password}
        }
        r = self.s.post(Config.WWF_HOST + url, json=data)
        return json.loads(r.text)


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
