from flask import Flask
import os
import wwf_client as WWF


"""
TODO
genericize this with a factory of clients
http://flask.pocoo.org/docs/0.12/cli/#factory-functions
"""


TITLE = 'Words With Fire'
app = Flask(__name__)


@app.route('/')
def home():
    disp = ""
    s = WWF.login(*get_credentials())
    games = WWF.get_games(s)
    for g in games:
        board = WWF.build_board_from_moves(g['moves'])
        board_str = WWF.board_to_str(board)
        disp += f'\n{board_str}\n'
    return f'<!DOCTYPE html>\n<html><body><pre>\n{disp}\n</pre></body></html>'


@app.cli.command()
def play():
    s = WWF.login(*get_credentials())
    games = WWF.get_games(s)
    for g in games:
        board = WWF.build_board_from_moves(g['moves'])
        print(WWF.board_to_str(board))
        print()


@app.cli.command()
def work():
    s = WWF.login(*get_credentials())
    r = WWF.get_daily_drip(s)
    print(r.json())


def get_credentials():
    username = os.environ.get('WWF_USER')
    password = os.environ.get('WWF_PASS')
    return (username, password)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
