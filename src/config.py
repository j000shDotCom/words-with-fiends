import os

class Config(object):
    TITLE = 'Words With Fiends'
    SHORT_TITLE = 'WWFIENDS'

    REDIS_URL = os.environ.get('REDIS_URL')
    PUSHER_URL = os.environ.get('PUSHER_URL')
    DATABASE_URL = os.environ.get('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WORDS_FILE = 'words.json.gz'
    WWF_HOST = 'https://wordswithfriends.zyngawithfriends.com'

    CLIENT_VERSION = 14.52
    BUNDLE_NAME = 'WordsWithFriends3'
    DEVICE_MODEL = 'iPhone'

