# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
# https://github.com/imwilsonxu/fbone

import os
from flask import Flask
from ..wwf_service import WwfService


def configure_app(app):
    from ..config import Config
    app.config.from_object(Config)

def configure_extensions(app):
    from ..wwf_service.extensions import setup_db
    setup_db(app)

def configure_routes(app):
    from .routes import web_routes
    app.register_blueprints(web_routes)


def create_app():
    app = Flask(__name__)
    configure_app(app)
    configure_routes(app)
    configure_extensions(app)
    return app


flask_app = create_app()
WWF = WwfService()

if __name__ == "__main__":
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    flask_app.run(HOST, PORT)
