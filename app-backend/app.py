import sqlite3
from flask import Flask, session
app = Flask(__name__)


# Set up database.
conn = sqlite3.connect('database.db')
c = conn.cursor()


@app.route("/<salary>/<location>")
def index(salary, location):
    nessie_id = 'dummy123'
    fc = FlowChart(nessie_id, salary, location)
    fc.load_default()
    fc.update_database()
    query2 = c.execute("SELECT * FROM users WHERE nessieID = '%s'" %
                       nessie_id).fetchall()

    return query2


@app.route("/createuser", methods=['GET', 'POST'])
def create_user():
    """ Creates user. """
    if request.method == 'POST':
        return redirect(url_for('index.html'))
    return render_template('createuser.html')


@app.route("/flowchart/<username>/<password>")
def flowchart(username, password):
    '''
    @param username, password
    * Queries the database with the given username & password
    * Returns a JSON object containing the list of cards with values.'''
    return ''


@app.route("/cards")
def cards():
    '''Returns a JSON object containing a list of cards.'''
    return ''


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
