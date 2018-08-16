from flask import Flask
import requests
app = Flask(__name__)


@app.route("/")
def hello():
	# print(urllib.request("http://www.mocky.io/v2/5b75c6932e00006200536216"))
	return "hello world"
@app.route("/test")
def test():
	return requests.get("http://www.mocky.io/v2/5b75c6932e00006200536216").text




if __name__ == "__main__":
	app.run(debug=True) # run this app