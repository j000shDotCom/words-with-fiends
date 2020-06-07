import os

class Config(object):
    TITLE = 'Words With Fiends'
    SHORT_TITLE = 'WWFIENDS'

    APP_SECRET = os.environ.get('APP_SECRET')

    REDIS_URL = os.environ.get('REDIS_URL')
    PUSHER_URL = os.environ.get('PUSHER_URL')
    DATABASE_URL = os.environ.get('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WORDS_FILE = 'words.json.gz'
    WWF_ZYNGA_HOST = 'https://api.zynga.com'
    WWF_HTTP2_HOST = 'https://wordswithfriends.zyngawithfriends.com'
    WWF_APP_ID = 5003741

    CLIENT_VERSION = 14.52
    BUNDLE_NAME = 'WordsWithFriends3'
    DEVICE_MODEL = 'iPhone'

    # SERVER_HOST = os.environ.get('SERVER_HOST', 'localhost')
    # SERVER_PORT = os.environ.get('SERVER_PORT', 5000)
