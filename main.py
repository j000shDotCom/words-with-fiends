"""
 Simple bot to log into and play WWF
"""
from requests import Session
from requests.auth import AuthBase


class WWFAuth(AuthBase):
    def __init__(self, login, password):
        self.login = login
        self.password = password

    def __call__(self, r):

        # do something with the request here
        return r


def main():
    s = Session()
    url = 'https://wordswithfriends.zyngawithfriends.com'
    # credential variables redacted
    querystring = {
        'bundle_name': 'WordsWithFriends3',
        'device_model': 'iPhone',
        'hash': hash_param,
        'zpid': zpid,
        'client_version': '10.26'
    }
    data = {
        'login_request': {
            'login': username,
            'password': password
        }
    }
    headers = {
        'User-agent': 'WordsWithFriends3/10.26',
        'zpid': zpid,
        'zdid': zdid,
        'wfpw': wfpw
    }

    s.get(url + '/jumps/config', params=querystring)
    r = s.post(url + '/sessions/create', json=data, headers=headers, params=querystring)
    print(r.status_code)
    print(r.text)


main()
