import sqlite3, requests, json
from flask import Flask, session, request
from analytics.helper import parseCSV
from analytics.dummy_data_generator import data_csv
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


@app.route("/update/<num>/<value>")
def update(num, value):
    test_nessie_id = '5b72dc8f322fa06b67793bb8'
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

# returns an array of numbers for all users with certain category
@app.route("/<salary>/<location>/<category>")
def returnBudgetArray(salary, location, category):
    test_nessie_id = '5b72dc8f322fa06b67793bb8'

    ## individualDictionary contains a dictionary of filtered budgetProfiles
    wholeArray = parseCSV(int(salary), str(location), data_csv())
    numArray = [];

    for individual in json.loads(wholeArray) :
        ## change the 0 to category when categoryArray is a dictionary
        numArray.append(individual["categoryArray"][0])

    return json.dumps(numArray)


# test endpoint to make a get request to card and user information
@app.route("/generateBudget", methods=['POST'])
def generateBudget() :
    parameters = request.get_json()
    income = parameters["income"]
    location = parameters["location"]

    dataArray = json.loads(getFC(income, location))
    ## now cardDataArray has all of the cards, we just want key value pairs
    budgets = {}

    for item in dataArray :
        name = item["name"]
        value = item["budgetted"]
        budgets[name] = value

    return json.dumps(budgets)


def getFC(income, location):

    # if(parameters["income"]) :
    #     income = parameters["income"]
    # if(parameters["location"]) :
    #     location = parameters["location"]
    test_nessie_id = '5b72dc8f322fa06b67793bb8'

    fc = FlowChart(test_nessie_id, income, location, True)
    fc.load_default()
    return fc.google_bot_json()

# actual endpoint to get correct values for the above values
@app.route("/generate", methods=['POST'])
def generate() :
    parameters = request.get_json()
    return null

    ## return the individualDictionary in json form
    # return json.dumps(individualDictionary)

# endpoint for dialogflow, POST request
@app.route("/dialogFlow", methods=['POST'])
def webhook():
    # returns a dictionary of the data from dialog flow
    data = request.get_json()
    data = data["queryResult"]["parameters"]

    testZipCode = "94016"
    # get card data from this server
    server_data = getFC(5000, testZipCode)

    dataArray = json.loads(server_data)

    ## now cardDataArray has all of the cards, we just want key value pairs
    budgets = {}

    for item in dataArray :
        name = item["name"]
        value = item["budgetted"]
        budgets[name] = value

    ## now budgets has the key value pairs

    input = {
        "income": str(data["income"]),
        "location": data["location"],
        "budgets": budgets
    }

    income = input["income"]
    location = input["location"]

    toReturn = {}
    message = "Hey whats up, your income is " + income
    message += ", your location is " + location
    message += ". You should budget: "
    for category, value in budgets.items() :
        message += str(value) + " for " + category + ", "

    message = message[:-2]

    toReturn["fulfillmentText"] = message

    #
    return json.dumps(toReturn)


if __name__ == '__main__':
    app.run(debug=True) # run this app
