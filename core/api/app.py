#!/usr/bin/env python
from flask import Flask

app = Flask(__name__)

@app.route('/config_api')
def index():
    return "OK"

@app.route('/config_api/login', methods=['GET', 'POST'])
def login():
    return "OK"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)