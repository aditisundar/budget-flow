from flask import Flask, request
import requests, json
from helper.py import helper
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
    individualDictionary = json.loads(helper.parseCSV(income, location))

    ## return the individualDictionary in json form
    return json.dumps(individualDictionary)


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
@app.route("/", methods=['POST'])
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
