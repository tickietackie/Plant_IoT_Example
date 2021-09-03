import paho.mqtt.client as mqtt
import time
import datetime
import json
import mysql.connector
config = {
        'user': 'plant2',
        'password': '',
        'host': '10.1.0.237',
        'database': 'plantiot',
        'port': '3306'
    }

def on_message(client, userdata, msg):

        print("message received " ,str(msg.payload.decode("utf-8")))
        data = json.loads(str(msg.payload.decode("utf-8")))
        database_insert_plantdata(data)

def database_insert_plantdata(json_data):
    #data prep
    data_transport_id = json_data['transport_id']
    data_id = json_data['id']
    data_sensor = json_data['sensor']
    data_humidity = json_data['humidity']
    data_temperature = json_data['temperature']
    #data time prep
    #data_time = json_data['time']
    #data_time = datetime.datetime.fromtimestamp(data_time).strftime('%Y-%m-%d %H:%M:%S')

    dbcon = mysql.connector.connect(**config)
    cursor = dbcon.cursor()

    #check id
    get_id = """select id from plant where mac_address = %s"""
    get_val = (data_id)
    cursor.execute(get_id, (data_id,))
    row = cursor.fetchone()
    if row == None:
        #create id when mac_address has no id
        print("Empty")
        create_id = "INSERT INTO plant (id,name,mac_adress)"
        create_val = ('','',data_id)
        cursor.execute(create_id,create_val)
        get_id = """select id from plant where mac_address = %s"""
        get_val = (data_id)
        cursor.execute(get_id, (data_id,))
        row = cursor.fetchone()
        data_plant_id=data_id
    else:
        data_plant_id=data_id

    val = (data_plant_id, data_temperature, data_humidity, data_transport_id, data_sensor,data_time)
    add_data = "INSERT INTO plant_data (plant_id, temp, humidity, transport_id, sensor, time) VALUES (%s,%s,%s,%s,%s,%s)"
    cursor.execute(add_data,val)
    dbcon.commit()
    cursor.close()
    dbcon.close()

#mqtt connection infos
client = mqtt.Client()
client.on_message = on_message
client.username_pw_set(username="casiot", password="casiot")
BROKER_ADDRESS = "mq.jreichwald.de"
client.connect(BROKER_ADDRESS)



if __name__ == "__main__":
        while True:
                client.loop_start()
                client.subscribe("plantDataGroup5")
                client.loop_stop()