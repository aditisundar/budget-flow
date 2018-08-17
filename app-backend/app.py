<<<<<<< HEAD
import sqlite3
from flask import Flask, session

from integration.flowchart import FlowChart
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)


conn = sqlite3.connect('database.db')
db = conn.cursor()


@app.route("/<salary>/<location>")
def index(salary, location):
    test_nessie_id = '5b72dc8f322fa06b67793bb8'

    # Creates FlowChart object, populates the flowchart, updates the database, and spits out JSON for front end.
    fc = FlowChart(test_nessie_id, int(salary), str(location), True)
    fc.load_default()
    fc.upsert_database()
    cardsObject = fc.front_end_json()
    return cardsObject

    # Code that should be run when editting one card
    #card_num = None
    #card_new_value = None
    #db.execute("""UPDATE users SET %s = WHERE nessieID = %i""" % ('f' + str(card_num), card_new_value))
    #fc = FlowChart(test_nessie_id, salary, zipcode, False)
    # fc.load_default()
    # fc.upsert_database()
    #cardsObject = fc.front_end_json()


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


if __name__ == '__main__':
    index()
=======
from flask import Flask, request
import requests, json
import helper
import dummy_data
app = Flask(__name__)


@app.route("/")
def hello():
    return "hello world"

# test enpoint to make a get request to card and user information
@app.route("/test")
def test():
    return requests.post("http://www.mocky.io/v2/5b75c6932e00006200536216").text

# actual endpoint to get correct values for the above values
@app.route("/generate", methods=['POST'])
def generate() :
    parameters = request.get_json()
    income = parameters["income"]
    location = parameters["location"]


    ## individualDictionary contains a dictionary of filtered budgetProfiles
    return helper.parseCSV(income, str(location), dummy_data.data_csv())

    ## return the individualDictionary in json form
    # return json.dumps(individualDictionary)


## function to take in income and location from dialogflow, budgetArray from
## the server
def fillDialogFlow(income, location, budgetArray) :
    toReturn = {}
    str = "Hey whats up, your income is " + income
    str += ", your location is " + location
    str += ", and "
    for category, value in budgetArray.items() :
        str += category + " - " + value
    toReturn["fulfillmentText"] = str
    return toReturn

# endpoint for dialogflow, POST request
@app.route("/dialogFlow", methods=['POST'])
def webhook():
    # returns a dictionary of the data from dialog flow
    # returns a dictionary of the data from dialog flow
    data = request.get_json()
    data = data["queryResult"]["parameters"]

    # get card data from this server
    server_data = test()
    cardDataArray = json.loads(server_data)["cards"]

    ## now cardDataArray has all of the cards, we just want key value pairs
    budgets = {}

    for card in cardDataArray :
        name = card["cardName"]
        value = card["cardExpense"]
        budgets[name] = value

    ## now budgets has the key value pairs

    input = {
        "income": str(data["income"]),
        "location": data["location"],
        "budgets": budgets
    }
    toReturn = fillDialogFlow(input["income"], input["location"], input["budgets"])

    return json.dumps(toReturn)


if __name__ == "__main__":
    app.run(debug=True) # run this app
