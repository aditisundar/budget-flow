from flask import Flask
import urllib
app = Flask(__name__)


@app.route("/")
def hello():
	print(urllib.request("http://www.mocky.io/v2/5b75c6932e00006200536216"))

@app.route("/test")
def test():
	return urllib.request("http://www.mocky.io/v2/5b75c6932e00006200536216")




if __name__ == "__main__":
	app.run(debug=True) # run this app