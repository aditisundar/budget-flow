import sqlite3
from flask import Flask, session
app = Flask(__name__)


@app.route("/")
def index():
    test_nessie_id = '5b72dc8f322fa06b67793bb8'
    salary = None
    zipcode =  None

    # Creates FlowChart object, populates the flowchart, updates the database, and spits out JSON for front end.
    fc = FlowChart(test_nessie_id, salary, zipcode, True)
    fc.load_default()
    fc.upsert_database()
    cardsObject = fc.front_end_json()
    return "Hello World!"


@app.route("/<username>/<password>/name=<name>")
def stats(username, password, name):
    '''
    @param username, password, name
    * Returns an array of values (boxplot style - 5 values: Q1, Q2, Median, Q3 & Q4).
    * Values should be calculated based on spending habits in said category of other people who fall under the same bracket as the user.
    * Ex: If the name is 'Food', then this should return a boxplot summary of how much people from the same (location, income, etc.) as the user spend on food monthly.
    '''
    return ''


if __name__ == '__main__':
    index()
