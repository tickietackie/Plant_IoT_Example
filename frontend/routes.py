from flask import Flask, render_template, redirect, url_for, request
import mysql.connector
db_connection = mysql.connector.connect(
    host="10.1.0.237",
    user="plant2",
    database="plantiot"
)
my_database = db_connection.cursor()

# making list of pokemons
plants = []

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/')
def homepage():
    sql_statement = "SELECT * FROM plant"
    my_database.execute(sql_statement)
    plants = my_database.fetchall()
    # making list of pokemons
    return render_template("index.html", len=len(plants), plants=plants)
    # return 'Hello, World!'


@app.route('/plantDetails')
def details():
    id = request.args.get("id")
    if id:
        sql_statement = f"SELECT * FROM plant_data where plant_id = {id}"
        my_database.execute(sql_statement)
        plants = my_database.fetchall()
        # making list of pokemons
        return render_template("details.html", len=len(plants), plants=plants)
        # return 'Hello, World!'
    else:
        return "Id missing in request."


@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success', name=user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success', name=user))

# "transport_id": 688989553,
    # "id": "8C:AA:B5:7C:F9:86",
    # "sensor": "DHT11",
    # "time": "09:46:01",
    # "humidity": 40,
    # "temperature": 24.7
