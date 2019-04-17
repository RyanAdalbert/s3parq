#!/usr/bin/env python
from datetime import datetime
import json, requests, os, sqlalchemy.orm
from flask import Flask, request, session
from core.helpers.configuration_mocker import ConfigurationMocker as CMock
from core.models.configuration import (
    PharmaceuticalCompany, 
    Brand,
    Pipeline,
    PipelineState, 
    PipelineType, 
    Segment,
    Administrator
)
try:
    from core.constants import BRANCH_NAME
    b = BRANCH_NAME
except Exception as e:
    b = e

def jsonify(self): # takes a defined db data class and serializes it into json
    data = self.__dict__.copy()
    del data['_sa_instance_state']
    for key, value in data.items():
        if(isinstance(value, datetime)):
            data[key] = value.strftime("%m/%d/%Y %H:%M")
    return json.dumps(data)

def queryjson(self):
    jstring = "{\n"
    for obj in query:
        key = obj.id
        val = jsonify(obj)
        jstring += "\"" + key + "\":" + val + ",\n"

def authorize(token, fsess):
    base = "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token="
    url = base + token
    resp = requests.get(url)
    if resp.status_code != 200:
        return False
    data = resp.json()
    email = data['email']
    sess = mocker.get_session()
    query = sess.query(Administrator).filter(Administrator.email_address==email)
    try:
        query.one()
        fsess['token'] = token
        return True
    except NoResultFound:
        return False

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)

mocker = CMock()
mocker.generate_mocks()
#app.register_blueprint(routes)

@app.route('/config_api')
def index():
    return "No request specified. Did you mean /api/login?"

@app.route('/config_api/login', methods=['GET', 'POST'])
def login():
    if request.method != 'POST':
        return "Error: Login token not specified."
    data = request.form 
    if not "token" in data:
        return "Error: Login token not specified."
    token = data['token']
    if authorize(token, session):
        return "Login good"
    else:
        return "Login bad"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)