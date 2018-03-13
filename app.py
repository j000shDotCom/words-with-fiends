from flask import Flask
import os
import wwf_client as WWF


"""
TODO
genericize this with a factory of clients
http://flask.pocoo.org/docs/0.12/cli/#factory-functions

Check Flask Classes
https://pythonhosted.org/Flask-Classy/

Flask Database connect to Postgres
http://flask.pocoo.org/docs/0.12/patterns/sqlalchemy/
"""


TITLE = 'Words With Fiends'
app = Flask(__name__)


@app.route('/')
def home():
    return test()

@app.route('/test')
def test():
    disp = ""
    s = WWF.login(*get_credentials())
    games = WWF.get_games(s)
    link = '<a href="https://cs.rit.edu/~jal3040/files/fiends.html">more</a>'
    for g in games:
        (board, st) = WWF.get_nums(g['moves'])
        disp += f'\n{st}\n'
    return f'<!DOCTYPE html>\n<html><body><pre>\n{disp}\n</pre>{link}</body></html>'

@app.cli.command()
def play():
    s = WWF.login(*get_credentials())
    games = WWF.get_games(s)
    for g in games:
        (board, st) = WWF.get_nums(g['moves'])


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
