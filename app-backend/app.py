import sqlite3
import requests
import json
from flask import Flask, session, request
from analytics.helper import parseCSV
from analytics.dummy_data_generator import data_csv
from analytics.helper2 import parseCSV2
from analytics.dummy_data_generator2 import data_csv2

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

# returns an array of numbers for all users with certain category


@app.route("/<salary>/<location>/<category>")
def returnBudgetArray(salary, location, category):
    test_nessie_id = '5b72dc8f322fa06b67793bb8'

    # individualDictionary contains a dictionary of filtered budgetProfiles
    wholeArray = parseCSV(int(salary), str(location), data_csv())
    numArray = []

    for individual in json.loads(wholeArray):
        # change the 0 to category when categoryArray is a dictionary
        num = individual["categoryArray"][int(category)]
        numArray.append(num)

    minVal = min(numArray)
    maxVal = max(numArray)
    interval = (maxVal - minVal)//5

    result = []

    for i in range(5):
        key = str(minVal + i*interval) + ' - ' + str(minVal + (i+1)*interval)
        result.append({"key": key, "value": 0})
        for num in numArray:
            if((num >= (minVal + i*interval)) and (num < (minVal + (i+1)*interval))):
                result[i]["value"] += 1

    return json.dumps(result)

# @app.route("/generateAverages", methods=['POST'])


def generateAverages(income, location):
    # parameters = request.get_json()
    # income = parameters["income"]
    # location = parameters["location"]

    # individualDictionary contains a dictionary of filtered budgetProfiles
    range = 0.25
    optional = False
    if(income == None):
        range = 15
        income = 3000
    if(location == None):
        optional = True
    wholeArray = parseCSV2(float(income), str(location),
                           data_csv2(), range, optional)
    averages = {}
    count = 0

    for individual in json.loads(wholeArray):
        # change the 0 to category when categoryArray is a dictionary
        for category, value in individual["categoryArray"].items():
            if(category in averages):
                averages[category] += value
            else:
                averages[category] = value

        count += 1

    for val in averages:
        averages[val] = int(averages[val] / count)

    return json.dumps(averages)

# test endpoint to make a get request to card and user information


@app.route("/generateBudget", methods=['POST'])
def generateBudget():
    parameters = request.get_json()
    income = parameters["income"]
    location = parameters["location"]

    dataArray = json.loads(getFC(income, location))
    # now cardDataArray has all of the cards, we just want key value pairs
    budgets = {}

    for item in dataArray:
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
def generate():
    parameters = request.get_json()
    return null

    # return the individualDictionary in json form
    # return json.dumps(individualDictionary)

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

    testZipCode = "94016"
    # get card data from this server
    server_data = getFC(5000, testZipCode)

    dataArray = json.loads(server_data)

    # now cardDataArray has all of the cards, we just want key value pairs
    budgets = {}

    for item in dataArray:
        name = item["name"]
        value = item["budgetted"]
        budgets[name] = value

    # now budgets has the key value pairs
    if("income" in data and len(str(data["income"])) > 0):
        income = str(data["income"])
    else:
        income = None

    if("location" in data and len(str(data["location"])) > 0):
        location = data["location"]
    else:
        location = None

    budgets = json.loads(generateAverages(income, location))

    if("category" in data and len(str(data["category"])) > 0):
        toReturn = {}
        value = budgets[data["category"]]
        message = "On average, people spend " + \
            str(value) + " on " + str(data["category"])
        toReturn["fulfillmentText"] = message
        return json.dumps(toReturn)

    toReturn = {}
    message = ""
    if(income != None):
        message += "For an income of " + income + " - "
    if(location != None):
        message += "A zip code in " + location + " - "

    message += "You should budget: "

    for category, value in budgets.items() :
        message += str(value) + " for " + category + ", "

    message = message[:-2]

    toReturn["fulfillmentText"] = message

    #
    return json.dumps(toReturn)


if __name__ == '__main__':
    app.run(debug=True)  # run this app
