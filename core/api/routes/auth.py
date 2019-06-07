from core.helpers.session_helper import SessionHelper as SHelp
import requests, sqlalchemy.orm
from flask import Flask, Blueprint, request, session
from core.models.configuration import Administrator

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
    sess.close()
    try:
        query.one()
        return True
    except sqlalchemy.orm.exc.NoResultFound:
        return False

def check_cookie(token): # checks for session cookie
    try:
        return token == session['Authorization']
    except KeyError:
        return False

@bp.route('')
def index():
    return "No request specified. Did you mean /config_api/login?"

@bp.route('/login', methods=['GET']) # Tokens must be submitted as form data in a POST request
def login():
    helper = SHelp()
    if not "Authorization" in request.headers:
        return "Login token not specified.", 401
    token = request.headers.get('Authorization')
    if authorize(token, helper):
        session['Authorization'] = token
        return "Login accepted"
    else:
        return "Bad login", 403

@bp.route('/validate', methods=['GET']) # Tokens must be submitted as form data in a POST request
def validate():
    if not "Authorization" in request.headers:
        return "Login token not specified.", 401
    if check_cookie(request.headers.get('Authorization')):
        return "Session token validated."
    else:
        return "Invalid session token.", 403