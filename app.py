from flask import Flask
import os
import wwf_client as WWF
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import psycopg2
from sqlalchemy.dialects.postgresql import ARRAY

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/wwfiends'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Move(db.Model):
    __tablename__ = "moves"
    id = db.Column(db.BigInteger, primary_key=True)
    game_id = db.Column(db.BigInteger)
    user_id = db.Column(db.BigInteger)
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
    words = db.ARRAY(db.String(80))
    data = None


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
def store():
    s = WWF.login(*get_credentials())
    games = WWF.get_games(s)
    for g in games:
        moves = g['moves']
        for m in moves:
            move = Move(**m)
            try:
                db.session.add(move)
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()


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
