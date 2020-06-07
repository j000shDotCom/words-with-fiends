from flask import Blueprint, flash, request, render_template, redirect, url_for

from . import WWF
from ..wwf_service.wwf_service import login_required

web_routes = Blueprint('web-routes', __name__)

@web_routes.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        login_result = WWF.login(*request.values)
        if login_result:
            flash("you've logged in!")
            return redirect(url_for('home'))
        else:
            flash('login failed', category='error')
            return redirect(url_for('login'))
    else:
        return "NO IDEA HOW I GOT HERE"

@login_required
@web_routes.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@login_required
@web_routes.route('/money/<money>')
def make_money_moves(money):
    pass # kinda just keeping this here to remember positional arguments


def get_credentials(user_env, pswd_env):
    if not user_env or not pswd_env:
        raise 'No environment variables provided'
    return os.environ.get(user_env), os.environ.get(pswd_env)
