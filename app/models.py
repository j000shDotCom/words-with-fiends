from datetime import datetime
from app import db

class Move(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
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
    id = db.Column(db.BigInteger, primary_key=True)
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
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(80))
    zynga_account_id = db.Column(db.BigInteger)

class Word(db.Model):
    __tablename__ = "words"
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(80), nullable=False, unique=True)
