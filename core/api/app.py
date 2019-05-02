#!/usr/bin/env python
from datetime import datetime
from flask_cors import CORS
import json, requests, os, sqlalchemy.orm
from flask import Flask, Blueprint, request, session
from core.api.routes import auth, index
from core.constants import BRANCH_NAME

def create_app()->Flask:
    app = Flask(__name__)
    app.secret_key = b'\xb6\xcf:v_\xffh\xfe\xa2\x82\xac\x8b\xd7qL\x07'
    app.register_blueprint(auth.bp, url_prefix="/config_api")
    app.register_blueprint(index.bp, url_prefix="/config_api")
    CORS(app, supports_credentials=True)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)