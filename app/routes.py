from os import environ
import json
import gzip
from app import app, db
from wwf_client.wwf import WWF

@app.route('/')
def show():
    w = WWF(*get_credentials())
    games = w.get_games()
    s = w.login(*get_credentials('MY_USER', 'MY_PASS'))
    games += w.get_games()

    html = '<!DOCTYPE html>\n<html bgcolor="black">\n<head>\n<meta charset="utf-8"/>\n'
    html += '\t<meta name="viewport" content="width=device-width, initial-scale=1"/>\n'
    html += '</head>\n<body>\n<pre>'

    for g in games:
        if 'moves' not in g:
            continue

        text_board = []
        num_board = []

        html += f"\n\n{[u['name'] for u in g['users']]}\n"
        boards = (
            [' '.join(l) for l in text_board],
            [' '.join(['{:3d}'.format(x) if x else '   ' for x in l]) for l in num_board]
        )
        for row in zip(*boards):
            html += f'\n\t{row[0]}\t\t{row[1]}'
    
    html += '\n</pre>\n</body>\n</html>\n'
    
    store_games(games)
    return html

@app.cli.command()
def play():
    w = WWF(*get_credentials())
    games = w.get_games()
    for g in games:
        if w.can_make_move(g):
            m = g.get_next_illegal_move()
            w.make_move(m)

@app.cli.command()
def work():
    w = WWF(*get_credentials())
    w.get_daily_drip()

@app.cli.command()
def store():
    w = WWF(*get_credentials())
    games = w.get_games()
    w.store_games(games, db)
    words()

## TODO move this out
def store_games(games):
    for g in games:
        users = g['users']
        moves = g['moves'] if 'moves' in g else []

        store_thing(UserModel, g['users'])
        store_thing(GameModel, [{k:g[k] for k in g if k not in ['moves', 'users']}])

        for m in moves:
            m['word'] = m['words'][0] if m['words'] else ''
        store_thing(MoveModel, moves)

## TODO move this out
def words():
    # json.dump([l.strip() for l in open('words.txt', 'r')], open('words.json', 'w'))
    # import shutil
    # with open('words.json', 'rt') as f_in:
    #     with gzip.open('words.json.gz', 'wt') as f_out:
    #         shutil.copyfileobj(f_in, f_out)
    words = [{'word': w} for w in json.load(gzip.open('words.json.gz', 'rb'))]
    store_thing(WordModel, words)

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
    username = environ.get(user_env)
    password = environ.get(pswd_env)
    return (username, password)
