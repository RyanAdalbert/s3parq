#!/usr/bin/env python
from flask import Flask
#from core.constants import BRANCH_NAME

app = Flask(__name__)

try:
    from core.constants import BRANCH_NAME
    b = BRANCH_NAME
except Exception as e:
    b = e

@app.route('/')
def hello_world():
    return f"hello CORE world! {b}"
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
