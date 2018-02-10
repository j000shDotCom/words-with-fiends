from flask import Flask
import os
import wwf_client as WWF


"""
TODO
genericize this with a factory of clients
http://flask.pocoo.org/docs/0.12/cli/#factory-functions
"""


TITLE = 'Words With Fire'
app = Flask(__name__)


@app.route('/')
def home():
    return """
<html>
    <head><title{title}</title></head>
    <body><h1>{title}</h1>
        <p>
            At some point I will make this browsable or playable.
            Until then, it'll just be a simple worker.
        </p>
    </body>
</html>
    """.format(title=TITLE)


@app.cli.command()
def play():
    print('TODO - and this is to test')
    pass


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
