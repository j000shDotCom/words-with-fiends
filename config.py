import os

class Config(object):
    TITLE = 'Words With Fiends'
    SHORT_TITLE = 'WWFIENDS'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WORDS_FILE = 'words.json.gz'
    CLIENT_VERSION = '10.26'
    BUNDLE_NAME = 'WordsWithFriends3'
    WWF_HOST = 'https://wordswithfriends.zyngawithfriends.com'

