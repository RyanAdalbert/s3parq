#!/usr/bin/env python
from flask import Flask
#from core.constants import BRANCH_NAME

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "hello CORE world!"
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
