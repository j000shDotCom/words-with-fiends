from requests import Session
from config import Config
import json

class WwfClient():
    def __init__(self, login, password):
        self.s = Session()
        self.s.hooks['response'].append(_log_request_status)
        self.s.headers.update({'Accept': 'application/json'})


    def initialize(self):
        self.get_auth_token()
        self.get_initial_config()
        self.user = User(self.login(login, password))
        self.misc_user_data = self.get_user_data()


    def login_with_email(self, email, password):
        #url = 'https://http2.api.zynga.com/gwf/password'
        url = 'https://http2.api.zynga.com/gwf/sessions/create'
        params = {
            'bundle_name': Config.BUNDLE_NAME,
            'device_model': Config.DEVICE_MODEL,
            'hash': '9ce926da851ea7652e23a44ddf064f6eee7fafe3',
            'zpid': '57A4F64E-DE57-4220-B002-1BCFEF210E2E',
            'client_version': Config.CLIENT_VERSION
        }
        payload = {
            'login_request': {
                'login': email,
                'password': password
            }
        }
        r = self.s.post(url, params=params, json=payload)
