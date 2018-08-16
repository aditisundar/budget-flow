from flask import Flask
app = Flask(__name__)


# import integration.flowchart

# Main page. Flow chart goes.
@app.route("/")
def hello():
    # flow chart loading code goes here
    return "Hello World!"



