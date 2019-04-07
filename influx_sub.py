import paho.mqtt.client as mqtt
from datetime import datetime
import time
from influxdb import InfluxDBClient
import json

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.subscribe("/sensors/dht22/")
    else:
        print("Connection failed"+str(rc))
    
def on_message(client, userdata, message):
    print("Received a message on topic: " + message.topic)
    data = message.payload.decode()
    print (data)
    try:
        jdata = json.loads(data)
    except Exception as e:
        print("Couldn't parse raw data: %s" % data, e)

    try:
        json_body = [
                {
                    "measurement": "temperature",
                    "tags": {
                        "location": "green house",
                        "region": "Wro-PL"
                    },
                    "time": datetime.today(),
                    "fields":{
                        "value": str(jdata["temperature"])
                    }
                }
            ]

        
        json_body1 = [
                {
                    "measurement": "hum",
                    "tags": {
                        "location": "green house",
                        "region": "Wro-PL"
                    },
                    "time": datetime.today(),
                    "fields":{
                        "value": str(jdata["humidity"])
                    }
                }
            ]
    except Exception as e:
        print(e)
    
    try:
        dbclient.write_points(json_body)
        dbclient.write_points(json_body1)
    except Exception as e:
        print("Failed writing to InfluxDB", e)
    else:
        print("Finished writing to InfluxDB")
        

dbclient = InfluxDBClient('localhost', 8086, 'admin', 'root', 'green_rpi')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 71)
client.loop_start()

try:
    while True:
        time.sleep(1) 
except KeyboardInterrupt:
    print ("exiting")
    client.disconnect()
    client.loop_stop()


