from flask import Flask, render_template, redirect, url_for, request
import mysql.connector
import json
import os
port = int(os.getenv("PORT"))

#get config and env variables
if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    if 'a9s-mysql101' in vcap:
        creds = vcap['a9s-mysql101'][0]['credentials']
        sqluser = creds['username']
        sqlpassword = creds['password']
        sqlhost = creds['host']
        sqlport = creds['port']
        sqldb = creds['name']

config = {
    'host' : sqlhost,
    'user' : sqluser,
    'password' : sqlpassword,
    'database' : sqldb,
    'port' : sqlport
    }


plants = []

app = Flask(__name__)
app.config["DEBUG"] = True

#display the location db
@app.route('/')
def homepage():
    dbconH = mysql.connector.connect(**config)
    cursorH = dbconH.cursor(buffered=True)
    sql_statement = "SELECT * FROM location"
    cursorH.execute(sql_statement)
    locations = cursorH.fetchall()
    # making list of pokemons
    cursorH.close()
    dbconH.close()
    return render_template("locations.html", len=len(locations), locations=locations)
  
    

#display the plantdetails
@app.route('/plantDetails')
def details():
    dbconP = mysql.connector.connect(**config)
    cursorP = dbconP.cursor(buffered=True)
    id = request.args.get("id")
    if id:
        sql_statement = f"SELECT * FROM plant_data where plant_id = {id}"
        cursorP.execute(sql_statement)
        plants = cursorP.fetchall()
        # making list of pokemons
        cursorP.close()
        dbconP.close()
        return render_template("details.html", len=len(plants), plants=plants)
        # return 'Hello, World!'
    else:
        return "Id missing in request."

#display the location
@app.route('/locations')
def location():
    dbconL = mysql.connector.connect(**config)
    cursorL = dbconL.cursor(buffered=True)
    sql_statement = "SELECT * FROM location"
    cursorL.execute(sql_statement)
    locations = cursorL.fetchall()
    cursorL.close()
    dbconL.close()
    # making list of pokemons
    return render_template("locations.html", len=len(locations), locations=locations)
    # return 'Hello, World!'

#display the area
@app.route('/location/area')
def area():
    dbconA = mysql.connector.connect(**config)
    cursorA = dbconA.cursor(buffered=True)
    id = request.args.get("location_id")
    if id:
        sql_statement = f"SELECT * FROM area where location_id = {id}"
        cursorA.execute(sql_statement)
        areas = cursorA.fetchall()
        # making list of pokemons
        cursorA.close()
        dbconA.close()
        return render_template("areas.html", len=len(areas), areas=areas)
        # return 'Hello, World!'
    else:
        return "Id missing in request."

#display all sensor data
@app.route('/location/area/sensor_data')
def sensor_data():
    dbconS = mysql.connector.connect(**config)
    cursorS = dbconS.cursor(buffered=True)
    id = request.args.get("area_id")
    if id:
        sql_statement = f"SELECT * FROM sensor_data where area_id = {id}"
        cursorS.execute(sql_statement)
        plants = cursorS.fetchall()
        # making list of pokemons
        cursorS.close()
        dbconS.close()
        return render_template("sensor_data.html", len=len(plants), plants=plants)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)