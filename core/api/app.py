#!/usr/bin/env python
from datetime import datetime
import json, requests, os, sqlalchemy.orm
from flask import Flask, Blueprint, request, session
from core.api import auth
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

'''
def queryjson(self):
    jstring = "{\n"
    for obj in query:
        key = obj.id
        val = jsonify(obj)
        jstring += "\"" + key + "\":" + val + ",\n"
'''

def create_app():
    app = Flask(__name__)
    app.secret_key = b'\xb6\xcf:v_\xffh\xfe\xa2\x82\xac\x8b\xd7qL\x07'
    app.register_blueprint(auth.bp)
    #app.register_blueprint(routes)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)