from flask import Flask
import os
import wwf_client as WWF
from database import db, Move, Game, User, Word
import json
import gzip

"""
TODO
genericize this with a factory of clients
http://flask.pocoo.org/docs/0.12/cli/#factory-functions

Check Flask Classes
https://pythonhosted.org/Flask-Classy/

Flask Database connect to Postgres
http://flask.pocoo.org/docs/0.12/patterns/sqlalchemy/

Djangoify!
"""

TITLE = 'Words With Fiends'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def show():
    disp = ""
    s = WWF.login(*get_credentials())
    games = WWF.get_games(s)
    link = '<a href="https://cs.rit.edu/~jal3040/files/fiends.html">more</a>'
    for g in games:
        (_, st) = WWF.get_nums(g['moves'])
        disp += f'\n{st}\n'
    return f'<!DOCTYPE html>\n<html><body><pre>\n{disp}\n</pre>{link}</body></html>'

@app.cli.command()
def play():
    s = WWF.login(*get_credentials())
    games = WWF.get_games(s)
    for g in games:
        (board, st) = WWF.get_nums(g['moves'])
        pass

@app.cli.command()
def work():
    s = WWF.login(*get_credentials())
    r = WWF.get_daily_drip(s)
    print(r.json())

@app.cli.command()
def store():
    s = WWF.login(*get_credentials())
    games = WWF.get_games(s)
    for g in games:
        store_game(g)

def store_game(game):
    store_users(game)
    store_moves(game['moves'])

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()

def store_users(game):
    for user in game['users']:
        u = User(**user)
        try:
            db.session.add(u)
        except Exception:
            db.session.rollback()

def store_moves(moves):
    for move in moves:
        move['word'] = move['words'][0]
        m = Move(**m)
        try:
            db.session.add(m)
        except Exception:
            db.session.rollback()

@app.cli.command()
def words():
    words = json.load(gzip.open('words.txt.gz', 'rb'))
    for w in words:
        try:
            word = Word(w)
            db.session.add(word)
        except Exception as e:
            db.session.rollback()
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()

def get_credentials(user_env = 'WWF_USER', pswd_env = 'WWF_PASS'):
    username = os.environ.get(user_env)
    password = os.environ.get(pswd_env)
    return (username, password)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
