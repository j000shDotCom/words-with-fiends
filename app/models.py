from datetime import datetime
from app import db
# TODO find some way to do this
# from app.db import Model, Boolean, Column, BigInteger, Integer, String, ARRAY, Float, ForeignKey, DateTime

class Move(db.Model):
    __tablename__ = 'moves'
    id = db.Column(db.BigInteger, primary_key=True)
    game_id = db.Column(db.BigInteger, db.ForeignKey('games.id'))
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
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
    __tablename__ = 'games'
    id = db.Column(db.BigInteger, primary_key=True)
    client_version = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    word = db.Column(db.String(80))
    current_move_user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    created_by_user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    is_fsn = db.Column(db.Boolean)
    is_matchmaking = db.Column(db.Boolean)
    was_matchmaking = db.Column(db.Boolean)
    random_seed = db.Column(db.BigInteger)
    create_type = db.Column(db.String(80))
    days_left = db.Column(db.Integer)
    game_data = db.Column(db.JSON)
    moves_count = db.Column(db.Integer)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(80))
    zynga_account_id = db.Column(db.BigInteger)

class Word(db.Model):
    __tablename__ = 'words'
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(80), nullable=False, unique=True)
