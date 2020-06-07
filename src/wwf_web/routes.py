import json
import gzip
from functools import wraps
from flask import flash, request, render_template, session, redirect, url_for

from ..wwf_service import WwfService
from . import app

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


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        return attempt_login(*request.values)
    else:
        return "NO IDEA HOW I GOT HERE"


def attempt_login(email, password):
    login_result = WwfService.login(email, password)
    print(login_result)
    if login_result:
        flash("you've logged in!")
        return redirect(url_for('home'))
    else:
        flash('login failed', category='error')
        return redirect(url_for('login'))


@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@login_required
@app.route('/money/<money>')
def make_money_moves(money):
    pass # kinda just keeping this here to remember positional arguments

def show():
    w = WWF(*get_credentials())
    games = w.get_games()
    s = w.login(*get_credentials('MY_USER', 'MY_PASS'))
    games += w.get_games()

    for g in games:
        if 'moves' not in g:
            continue

        render_template('partials/_board.html', g)
        text_board = []
        num_board = []

        html += f"\n\n{[u['name'] for u in g['users']]}\n"
        boards = (
            [' '.join(l) for l in text_board],
            [' '.join(['{:3d}'.format(x) if x else '   ' for x in l]) for l in num_board]
        )
        for row in zip(*boards):
            html += f'\n\t{row[0]}\t\t{row[1]}'

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


def get_credentials(user_env, pswd_env):
    if not user_env or not pswd_env:
        raise 'No environment variables provided'
    return environ.get(user_env), environ.get(pswd_env)
