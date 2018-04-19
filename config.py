import os

class Config(object):
    TITLE = 'Words With Fiends'
    SHORT_TITLE = 'WWFIENDS'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
