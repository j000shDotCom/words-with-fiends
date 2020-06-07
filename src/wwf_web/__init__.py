# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from ..config import Config

# https://github.com/imwilsonxu/fbone

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)


def configure_extensions():
    pass


def configure_cli():
    pass


def start_server():
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)

if __name__ == "__main__":
    start_server()

from . import routes
