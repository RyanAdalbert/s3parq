from core.helpers.session_helper import SessionHelper as SHelp
import requests
import sqlalchemy.orm
from flask import Flask, Blueprint, request, session
from core.models.configuration import (
    Administrator
)

bp = Blueprint('auth', __name__)

def parse_oauth(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        raise LookupError("Error: Invalid OAuth response")
    data = resp.json()
    if 'email' not in data:
        raise LookupError("Error: No email address returned from OAuth response.")
    email = data['email']
    return email

def authorize(token, session_helper): # the token passed here needs to be generated elsewhere, e.g. a React frontend
    base = "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token="
    url = base + token
    try:
        email = parse_oauth(url)
    except LookupError:
        return False
    sess = session_helper.session
    query = sess.query(Administrator).filter(Administrator.email_address==email)
    try:
        query.one()
        return True
    except sqlalchemy.orm.exc.NoResultFound:
        return False

def check_cookie(token): # checks for session cookie
    try:
        return token == session['token']
    except KeyError:
        return False

@bp.route('/config_api')
def index():
    return "No request specified. Did you mean /config_api/login?"

@bp.route('/config_api/login', methods=['GET', 'POST']) # Tokens must be submitted as form data in a POST request
def login():
    helper = SHelp()
    if request.method != 'POST':
        return "Error: Only POST requests supported. Pass the token along as form data in your request.", 405
    data = request.form 
    if not "token" in data:
        return "Login token not specified.", 400
    token = data['token']
    if authorize(token, helper):
        session['token'] = token
        return "Login accepted"
    else:
        return "Bad login", 403

@bp.route('/config_api/validate', methods=['GET', 'POST']) # Tokens must be submitted as form data in a POST request
def validate():
    if request.method != 'POST':
        return "Error: Only POST requests supported. Pass the token along as form data in your request.", 405
    data = request.form
    if not "token" in data:
        return "No session cookie found!", 400
    if check_cookie(data['token']):
        return "Session token validated."
    else:
        return "Invalid session token.", 403