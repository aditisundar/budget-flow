from flask import Flask
app = Flask(__name__)



@app.route("/")
def index():
    # flow chart loading code goes here
    return "Hello World!"



