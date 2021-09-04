import paho.mqtt.client as mqtt
import time
import datetime
import json
import mysql.connector
import cred

config = {
        'user': cred.login['db_user'],
        'password': cred.login['db_password'],
        'host': cred.login['host'],
        'database': cred.login['database'],
        'port': cred.login['port']
    }

def on_message(client, userdata, msg):

        print("message received " ,str(msg.payload.decode("utf-8")))
        data = json.loads(str(msg.payload.decode("utf-8")))
        database_location_id(data)
               

def database_location_id(json_data)
    dbconL = mysql.connector.connect(**config)
    cursorL = dbconL.cursor()
    loc_id = json_data['location_id']
    set_loc = "INSERT IGNORE INTO location (id, name) VALUES(%s,%s)"
    val_loc = (loc_id,"")
    cursorL.execute(set_loc, (val_loc,))
    dbconL.commit()
    cursorL.close()
    dbconL.close()
    database_check_area_id(data,loc_id) 

def database_check_area(json_data,loc_id):
    dbconA = mysql.connector.connect(**config)
    cursorA = dbconC.cursor()
    data_id = json_data['area_id']
    get_id = "select id from area where mac_address = %s"
    get_val = (data_id)
    cursorA.execute(get_id, (data_id,))
    row = cursorA.fetchone()
    if row == None:
        #create id when mac_address has no id
        create_id = "INSERT INTO area (location_id,mac_address) VALUES(%s,%s)"
        create_val = (loc_id,data_id)
        cursorA.execute(create_id,create_val)
        dbconA.commit()
        get_id = """select id from area where mac_address = %s"""
        get_val = (data_id)
        cursorA.execute(get_id, (data_id,))
        row = cursorA.fetchone()
        data_id = row[0]
        cursorA.close()
        dbconA.close()
        database_insert_sensordata(json_data,data_id)
    else:
        data_id = row[0]
        database_insert_sensordata(json_data,data_id)

def database_insert_sensordata(json_data,area_id):
    #data prep
    if 'transport_id' in json_data:
        data_sensor_transport_id = json_data['transport_id']
    else:
        return

    #data time prep
    try:
        data_time = json_data['time']
        data_sensor_time = datetime.datetime.fromtimestamp(data_time).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return

    data_sensor_area_id = area_id
    for x in range(0,3):
        dbconI = mysql.connector.connect(**config)
        cursorI = dbconC.cursori()
        data_sensor_value = json_data['sensor'][i]['value']
        data_sensor_unit = json_data['sensor'][i]['unit']
        data_sensor_type = json_data['sensor'][i]['type']
        data_sensor_name = json_data['sensor'][i]['name']
        add_data = "INSERT INTO plant_data (area_id, name, value, unit, type, time, transport_id) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        val = (data_sensor_area_id, data_sensor_name, data_sensor_value, data_sensor_unit, data_sensor_type, data_sensor_time, data_sensor_transport_id)
        cursorI.execute(add_data,val)
        dbconI.commit()
        cursorI.close()
        dbconI.close()   

#mqtt connection info
client = mqtt.Client()
client.on_message = on_message
client.username_pw_set(username=cred.login['mqtt_user'], password=cred.login['mqtt_password'])
BROKER_ADDRESS = cred.login['brokeraddress']
client.connect(BROKER_ADDRESS)

if __name__ == "__main__":
        while True:
                client.loop_start()
                client.subscribe(cred.login['mqtt_topic'])
                client.loop_stop()