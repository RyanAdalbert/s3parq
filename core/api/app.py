#!/usr/bin/env python
from flask import Flask
try:
    import helpers
    banana = "winner!"
except:
    banana = "loser"

app = Flask(__name__)

@app.route('/')
def hello_world():
    return f"hello CORE world! {banana}"
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
