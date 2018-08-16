# FLASK_APP=server.py FLASK_DEBUG=1 python -m flask run
from flask import Flask, render_template, Response
import json
from flask_cors import CORS, cross_origin
import utilities
import requests

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "Hello World!"


if __name__ == "__main__":
    app.run(threaded=True)
