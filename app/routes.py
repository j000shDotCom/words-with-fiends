import wwf_client as WWF
import os
import json
import gzip
from app import app, db
from app.models import User, Word, Game, Move

@app.route('/')
@app.route('/index')
def show():
    disp = ""
    s = WWF.login(*get_credentials())
    games = WWF.get_games(s)
    s = WWF.login(*get_credentials('MY_USER', 'MY_PASS'))
    games += WWF.get_games(s)
    html = '<!DOCTYPE html>\n<html>\n<head>\n<meta charset="utf-8"/>\n'
    html += '\t<meta name="viewport" content="width=device-width, initial-scale=1"/>\n'
    html += '</head>\n<body>\n<pre>\n'
    disp = ''
    for g in games:
        (_, st) = WWF.get_nums(g['moves'])
        disp += f"\n{[u['name'] for u in g['users']]}\n"
        disp += f"\n{st}\n"
    html += disp + '\n</pre>\n</body>\n</html>'
    store_games(games)
    return html


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
    store_games(games)

def store_games(games):
    for g in games:
        store_thing(User, g['users'])
        moves = g['moves']
        del g['users']
        del g['moves']
        store_thing(Game, [g])
        for m in moves:
            m['word'] = m['words'][0] if m['words'] else ''
        store_thing(Move, moves)

@app.cli.command()
def words():
    # json.dump([l.strip() for l in open('words.txt', 'r')], open('words.json', 'w'))
    # import shutil
    # with open('words.json', 'rt') as f_in:
    #     with gzip.open('words.json.gz', 'wt') as f_out:
    #         shutil.copyfileobj(f_in, f_out)
    words = [{'word': w} for w in json.load(gzip.open('words.json.gz', 'rb'))]
    store_thing(Word, words)

def store_thing(CL, objs):
    try:
        for ob in objs:
            e = CL(**ob)
            db.session.merge(e)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def get_credentials(user_env='WWF_USER', pswd_env='WWF_PASS'):
    username = os.environ.get(user_env)
    password = os.environ.get(pswd_env)
    return (username, password)
