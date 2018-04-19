import wwf_client as WWF
from app import app, db
import os
import json
import gzip
from app.models import User, Word, Game, Move

@app.route('/')
@app.route('/index')
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

@app.cli.command()
def words():
    words = json.load(gzip.open('words.txt.gz', 'rb'))
    store_words(words)


def store_game(game):
    store_users(game['users'])
    #store_moves(game['moves'])

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)

def store_users(users):
    for u in users:
        user = User(**u)
        try:
            db.session.merge(user)
        except Exception:
            db.session.rollback()
    
    db.session.commit()

def store_moves(moves):
    for m in moves:
        m['word'] = m['words'][0] if m['words'] else ''
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

def get_credentials(user_env = 'WWF_USER', pswd_env = 'WWF_PASS'):
    username = os.environ.get(user_env)
    password = os.environ.get(pswd_env)
    return (username, password)
