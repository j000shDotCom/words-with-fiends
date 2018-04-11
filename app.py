from flask import Flask
import os
import wwf_client as WWF
import database as db
import json
import gzip

from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
from flask_sqlalchemy import SQLAlchemy
import psycopg2

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

db = SQLAlchemy(app)


class Move(db.Model):
    __tablename__ = "moves"
    id = db.Column(db.BigInteger, primary_key = True)
    game_id = db.Column(db.BigInteger, db.ForeignKey('game.id'))
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    move_type = db.Column(db.String(80))
    from_x = db.Column(db.Integer)
    from_y = db.Column(db.Integer)
    to_x = db.Column(db.Integer)
    to_y = db.Column(db.Integer)
    move_index = db.Column(db.Integer)
    text = db.Column(db.String(80))
    board_checksum = db.Column(db.BigInteger)
    points = db.Column(db.Integer)
    promoted = db.Column(db.Integer)
    word = db.Column(db.String(80))
    words = db.Column(db.ARRAY(db.String(80)))
    data = None

class Game(db.Model):
    __tablename__ = "games"
    id = db.Column(db.BigInteger, primary_key = True)
    client_version = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    word = db.Column(db.String(80))
    current_move_user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'))
    created_by_user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'))
    is_fsn = db.Column(db.Boolean)
    is_matchmaking = db.Column(db.Boolean)
    was_matchmaking = db.Column(db.Boolean)
    move_count = db.Column(db.Integer)
    random_seed = db.Column(db.BigInteger)
    create_type = db.Column(db.String(80))

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.BigInteger, primary_key = True)
    name = db.Column(db.String(80))
    zynga_account_id = db.Column(db.BigInteger)

class Word(db.Model):
    __tablename__ = "words"
    id = db.Column(db.Integer, primary_key = True)
    word = db.Column(db.String(80))



def store_game(game):
    store_users(game['users'])
    store_moves(game['moves'])

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()

def store_users(users):
    for u in users:
        user = User(**u)
        try:
            db.session.add(user)
        except Exception:
            db.session.rollback()
    for u in User.query.all():
        print(u)

def store_moves(moves):
    for m in moves:
        m['word'] = m['words'][0]
        move = Move(**m)
        try:
            db.session.add(move)
        except Exception:
            db.session.rollback()

def store_words(words):
    for w in words:
        try:
            word = Word(w)
            db.session.add(word)
        except Exception:
            db.session.rollback()
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()



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
        db.store_game(g)

@app.cli.command()
def words():
    words = json.load(gzip.open('words.txt.gz', 'rb'))
    db.store_words(words)

def get_credentials(user_env = 'WWF_USER', pswd_env = 'WWF_PASS'):
    username = os.environ.get(user_env)
    password = os.environ.get(pswd_env)
    return (username, password)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
