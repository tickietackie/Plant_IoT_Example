import paho.mqtt.client as mqtt
import thingspeak
import time

channel_id = 1027843
write_key = '9QDWO94MA952NBLM'
channel = thingspeak.Channel(id=channel_id, write_key=write_key)

def on_message(client, userdata, message):
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message topic ", message.topic)
        print("message qos=",message.qos)
        print("message retain flag=",message.retain)
        if message.topic == 'esp32/temperature':
                global temp_value
                temp_value = str(message.payload.decode("utf-8"))
        if message.topic == 'esp32/humidity':
                global humi_value
                humi_value = str(message.payload.decode("utf-8"))
        if message.topic == 'esp32/window_closed':
                global win_value
                win_value = str(message.payload.decode("utf-8"))
        if message.topic != '':
                if temp_value != 0 and humi_value != 0:
                        response = channel.update({'field1':temp_value,'field2':humi_value,'field3':win_value})
                        print("Update")
                        time.sleep(15)
                        temp_value=0
                        humi_value=0
                        win_value=0

BROKER_ADDRESS = "172.20.10.3"
client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER_ADDRESS)

if __name__ == "__main__":
        while True:
                client.loop_start()
                client.subscribe("esp32/temperature")
                client.subscribe("esp32/humidity")
                client.subscribe("esp32/window_closed")
                client.loop_stop()