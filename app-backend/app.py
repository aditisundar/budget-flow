import sqlite3
import requests
import json
from flask import Flask, session, request
from analytics.helper import parseCSV
from analytics.dummy_data_generator import data_csv
from integration.flowchart import FlowChart
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)


def upsert_database(chart, nessie_id):
    """ Pass updated budgetted values to database. """
    conn = sqlite3.connect('database.db')
    db = conn.cursor()
    tup = tuple([card.budgetted for card in chart] + [nessie_id])
    update_query = """
        UPDATE
            users
        SET
            f1 = %f,
            f2 = %f,
            f3 = %f,
            f4 = %f,
            f5 = %f,
            f6 = '%s',
            f7 = %f,
            f8 = %f,
            f9 = %f,
            f10 = '%s',
            f11 = %f,
            f12 = '%s',
            f13 = %f,
            f14 = %f,
            f15 = %f,
            f16 = %f,
            f17 = %f,
            f18 = %f
        WHERE
            nessieID = '%s'
    """ % tup
    db.execute(update_query)
    conn.commit()
    conn.close()


@app.route("/<salary>/<location>")
def index(salary, location):
    test_nessie_id = '5b72dc8f322fa06b67793bb8'

    # Creates FlowChart object, populates the flowchart, updates the database, and spits out JSON for front end.
    fc = FlowChart(test_nessie_id, int(salary), str(location), True)
    fc.load_default()
    upsert_database(fc.chart, test_nessie_id)
    cardsObject = fc.front_end_json()
    return cardsObject


@app.route("/update/<salary>/<location>/<num>/<value>")
def update(salary, location, num, value):
    test_nessie_id = '5b72dc8f322fa06b67793bb8'
    # Code that should be run when editting one card
    conn = sqlite3.connect('database.db')
    db = conn.cursor()
    card_num = int(num)
    card_new_value = int(value)
    db.execute("""UPDATE users SET %s = %f WHERE nessieID = '%s'""" %
               ('f' + str(card_num), card_new_value, test_nessie_id))
    conn.commit()
    conn.close()
    fc = FlowChart(test_nessie_id, int(salary), str(location), False)
    fc.load_default()
    # fc.upsert_database()
    cardsObject = fc.front_end_json()
    return cardsObject


@app.route("/<username>/<password>/name=<name>")
def stats(username, password, name):
    '''
    @param username, password, name
    * Returns an array of values (boxplot style - 5 values: Q1, Q2, Median, Q3 & Q4).
    * Values should be calculated based on spending habits in said category of other people who fall under the same bracket as the user.
    * Ex: If the name is 'Food', then this should return a boxplot summary of how much people from the same (location, income, etc.) as the user spend on food monthly.
    '''
    return ''


@app.route("/bot_backend")
def bot_backend():
    test_nessie_id = '5b72dc8f322fa06b67793bb8'
    salary = None
    zipcode = None
    fc = FlowChart(test_nessie_id, salary, zipcode, True)
    fc.load_default()
    return fc.google_bot_json()


# test endpoint to make a get request to card and user information
@app.route("/test")
def test():
    return requests.post("http://www.mocky.io/v2/5b75c6932e00006200536216").text

# actual endpoint to get correct values for the above values


@app.route("/generate", methods=['POST'])
def generate():
    parameters = request.get_json()
    income = parameters["income"]
    location = parameters["location"]

    # individualDictionary contains a dictionary of filtered budgetProfiles
    return parseCSV(income, str(location), data_csv())

    # return the individualDictionary in json form
    # return json.dumps(individualDictionary)


# function to take in income and location from dialogflow, budgetArray from
# the server
def fillDialogFlow(income, location, budgetArray):
    toReturn = {}
    str = "Hey whats up, your income is " + income
    str += ", your location is " + location
    str += ", and "
    for category, value in budgetArray.items():
        str += category + " - " + value
    toReturn["fulfillmentText"] = str
    return toReturn

# endpoint for dialogflow, POST request


@app.route("/dialogFlow", methods=['POST'])
def webhook():
    # returns a dictionary of the data from dialog flow
    data = request.get_json()
    data = data["queryResult"]["parameters"]

    # get card data from this server
    server_data = test()
    cardDataArray = json.loads(server_data)["cards"]

    # now cardDataArray has all of the cards, we just want key value pairs
    budgets = {}

    for card in cardDataArray:
        name = card["cardName"]
        value = card["cardExpense"]
        budgets[name] = value

    # now budgets has the key value pairs

    input = {
        "income": str(data["income"]),
        "location": data["location"],
        "budgets": budgets
    }
    toReturn = fillDialogFlow(
        input["income"], input["location"], input["budgets"])

    return json.dumps(toReturn)


if __name__ == '__main__':
    app.run(debug=True)  # run this app
