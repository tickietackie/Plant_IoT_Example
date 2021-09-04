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
        database_check_ids(data)

def database_check_ids(json_data):
    dbconC = mysql.connector.connect(**config)
    cursorC = dbconC.cursor()
    data_id = json_data['id']
    get_id = "select id from plant where mac_address = %s"
    get_val = (data_id)
    cursorC.execute(get_id, (data_id,))
    row = cursorC.fetchone()
    data_id = row[0]
    if row == None:
        #create id when mac_address has no id
        create_id = "INSERT INTO plant (name,mac_address) VALUES(%s,%s)"
        create_val = ('',data_id)
        cursorC.execute(create_id,create_val)
        dbcon.commit()
        get_id = """select id from plant where mac_address = %s"""
        get_val = (data_id)
        cursorC.execute(get_id, (data_id,))
        data_id = cursorC.fetchone()
        cursorC.close()
        dbconC.close()
        database_insert_plantdata(json_data,data_id)
    else:
        database_insert_plantdata(json_data,data_id)

def database_insert_plantdata(json_data,db_id):
    #data prep
    data_transport_id = json_data['transport_id']
    data_plant_id = db_id
    data_sensor = json_data['sensor']
    data_humidity = json_data['humidity']
    data_temperature = json_data['temperature']
    #data time prep
    data_time = json_data['time']
    data_time = datetime.datetime.fromtimestamp(data_time).strftime('%Y-%m-%d %H:%M:%S')

    dbcon = mysql.connector.connect(**config)
    cursor = dbcon.cursor()  
    val = (data_plant_id, data_temperature, data_humidity, data_transport_id, data_sensor,data_time)
    add_data = "INSERT INTO plant_data (plant_id, temp, humidity, transport_id, sensor, time) VALUES (%s,%s,%s,%s,%s,%s)"
    cursor.execute(add_data,val)
    dbcon.commit()
    cursor.close()
    dbcon.close()

#mqtt connection infos
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