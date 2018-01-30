from flask import Flask
from datetime import datetime


app = Flask(__name__)


@app.route('/')
def home():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")
    return "Words With Fire! Time is now {time}".format(time=the_time)


@app.route('/reward')
def work():
    pass


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
