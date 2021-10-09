import paho.mqtt.client as mqtt
import time
import datetime
import json
import mysql.connector
import os
import cred

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
        'user': sqluser,
        'password': sqlpassword,
        'host': sqlhost,
        'database': sqldb,
        'port': sqlport
    }

#mqtt on message listener
def on_message(client, userdata, msg):
        print("message received " ,str(msg.payload.decode("utf-8")))
        data = json.loads(str(msg.payload.decode("utf-8")))
        database_location_set_id(data)

#check for location id 
def database_location_id(json_data):
    dbconN = mysql.connector.connect(**config)
    cursorN = dbconN.cursor(buffered=True)
    loc_id = json_data['location_id']
    query_get_loc = f"select * from location where id = {loc_id}"
    cursorN.execute(query_get_loc)
    msg=cursorN.fetchall()
    dbconN.commit()
    cursorN.close()
    dbconN.close()

#create a location id
def database_location_set_id(json_data):
    dbconL = mysql.connector.connect(**config)
    cursorL = dbconL.cursor(buffered=True)
    loc_id = json_data['location_id']
    loc_name = cred.login['location_name']
    query_set_loc = f"""insert ignore into  location (id, name) VALUES ({loc_id}, '{loc_name}')"""
    cursorL.execute(query_set_loc)
    dbconL.commit()
    cursorL.close()
    dbconL.close()
    database_check_area(json_data,loc_id)

#registere device
def database_check_area(json_data,loc_id):
    dbconA = mysql.connector.connect(**config)
    cursorA = dbconA.cursor(buffered=True)
    data_id = json_data['area_id']
    get_id = f"""select id from area where mac_address = '{data_id}'"""
    cursorA.execute(get_id)
    row = cursorA.fetchone()
    if row == None:
        create_id = f"""insert ignore area (location_id,mac_address) VALUES({loc_id},'{data_id}')"""
        cursorA.execute(create_id)
        dbconA.commit()
        database_check_area(json_data,loc_id)
        cursorA.close()
        dbconA.close()
    else:
        cursorA.close()
        dbconA.close()
        area_id=row[0]
        database_insert_sensordata(json_data,area_id)

#make sensor data usable for the db an insert them
def database_insert_sensordata(json_data,area_id):
    if 'transport_id' in json_data:
        data_sensor_transport_id = json_data['transport_id']
    else:
        return
    try:
        data_time = json_data['time']
        data_sensor_time = datetime.datetime.fromtimestamp(data_time).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return
    dbconS = mysql.connector.connect(**config)
    cursorS = dbconS.cursor(buffered=True)
    i = 0
    while i < 3:
        data_sensor_value = json_data['sensor'][i]['value']
        data_sensor_unit = json_data['sensor'][i]['unit']
        data_sensor_type = json_data['sensor'][i]['type']
        data_sensor_name = json_data['sensor'][i]['name']
        query_sensor_set = f"""insert into sensor_data (area_id, name, value, unit, type, time, transport_id) VALUES('{area_id}','{data_sensor_name}','{data_sensor_value}','{data_sensor_unit}','{data_sensor_type}','{data_sensor_time}','{data_sensor_transport_id}')"""
        print (query_sensor_set)
        cursorS.execute(query_sensor_set)
        dbconS.commit()
        i=i+1
    cursorS.close()
    dbconS.close()

#mqtt connection info
client = mqtt.Client()
client.on_message = on_message
client.username_pw_set(username=cred.login['mqtt_user'], password=cred.login['mqtt_password'])
BROKER_ADDRESS = cred.login['brokeraddress']
client.connect(BROKER_ADDRESS)

if __name__ == "__main__":
        while True:
                client.loop_start()
                client.subscribe('plantDataGroup5')
                client.loop_stop()