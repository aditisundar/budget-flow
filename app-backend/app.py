from flask import Flask, request
import requests
app = Flask(__name__)


@app.route("/")
def hello():
	return "hello world"

# test enpoint to make a get request to card and user information
@app.route("/test")
def test():
	return requests.get("http://www.mocky.io/v2/5b75c6932e00006200536216").text

# endpoint for dialogflow, POST request
@app.route("/", methods=['POST'])
def webhook():
	# returns a dictionary of the data from dialog flow
	data = request.get_json()

	# get card data from this server
	server_data = test()
	return data["first_name"] + server_data


if __name__ == "__main__":
	app.run(debug=True) # run this app