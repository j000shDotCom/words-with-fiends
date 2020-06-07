import json
import gzip
from functools import wraps
from flask import session

from ..wwf_client import WwfClient


class WwfService():
    def __init__(self):
        pass

    def login(self, login, password):
        wwf = WwfClient()
        r = wwf.login_with_email(login, password)
        print(r)
        return r

    def list_games(self, user):
        pass

    def make_game(self, type, user, challenger):
        pass

    def get_rewards(self, user):
        pass

    def make_move(self, game, user):
        pass

    def list_moves(self, game, user):
        pass


def login_required(function_to_protect):
    @wraps(function_to_protect)
    def wrapper(*args, **kwargs):
        user_id = session.get('user_id')
        if user_id:
            user = database.get(user_id)
            if user:
                # Success!
                return function_to_protect(*args, **kwargs)
            else:
                flash("Session exists, but user does not exist (anymore)")
                return redirect(url_for('login'))
        else:
            flash("Please log in")
            return redirect(url_for('login'))

def load_words(self, word_file_path):
    # json.dump([l.strip() for l in open('words.txt', 'r')], open('words.json', 'w'))
    # import shutil
    # with open('words.json', 'rt') as f_in:
    #     with gzip.open('words.json.gz', 'wt') as f_out:
    #         shutil.copyfileobj(f_in, f_out)
    word_file = gzip.open('words.json.gz', 'rb')
    words = [{'word': w} for w in json.load(word_file)]
    store_thing(WordModel, words)
