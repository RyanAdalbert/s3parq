from core.helpers.session_helper import SessionHelper as SHelp
import requests, sqlalchemy.orm, json
from flask import Blueprint, request
import core.api.routes.auth as auth
from core.models.configuration import (
    Pipeline,
    Brand,
    PharmaceuticalCompany
)

bp = Blueprint('index', __name__)

@bp.route('/index', methods=['GET', 'POST'])
def index():
    if request.method != "POST":
        return "Error: Only POST requests supported. Pass the token along as form data in your request.", 405
    data = request.form
    if not "token" in data:
        return "No session cookie found!", 400
    if not auth.check_cookie(data['token']):
        return "Invalid session token.", 403
    helper = SHelp()
    sess = helper.session
    query = sess.query(Pipeline).all()
    toJSON = {}
    for pl in query:
        key = pl.id
        pl_data = {}
        pl_data['name'] = pl.name
        pl_data['brand'] = pl.brand.name
        pl_data['pharma_company'] = pl.brand.pharmaceutical_company.name
        if pl.is_active:
            pl_data['status'] = "Active"
        else:
            pl_data['status'] = "Inactive"
        pl_data['description'] = pl.description
        pl_data['run_freq'] = pl.run_frequency
        toJSON[key] = pl_data
    return json.dumps(toJSON), 200