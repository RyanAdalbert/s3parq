#!/usr/bin/env python
from datetime import datetime
import json
from flask import Flask, request
from core.helpers.configuration_mocker import ConfigurationMocker as CMock
from core.models.configuration import (
    PharmaceuticalCompany, 
    Brand, 
    Pipeline, 
    PipelineType, 
    Segment
)

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

mocker = CMock()
mocker.generate_mocks()
session = mocker.get_session()

query = session.query(Brand).all()

try:
    from core.constants import BRANCH_NAME
    b = BRANCH_NAME
except Exception as e:
    b = e

app = Flask(__name__)
#app.register_blueprint(routes)
with app.app_context():
    print(jsonify(query))

@app.route('/api')
def index():
    return "No request specified. Did you mean /api/login?"

@app.route('/api/login')
def login():
    if request.method != 'POST':
        return "Error: Login information not specified."


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)