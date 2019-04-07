import paho.mqtt.client as mqttClient
import time
import json
 
def on_connect(client, userdata, flags, rc): 
    if rc == 0: 
        print("Connected to broker")
        client.subscribe("/sensors/dht22/")
    else: 
        print("Connection failed"+str(rc))

 
def on_message(client, userdata, message):
    print (message.topic)
    data = message.payload.decode()
    print ("Current conditions: "  + data)
    
    jdata = json.loads(data)
    print (jdata["temperature"])
    print (type(jdata["temperature"]))
 
broker_address= "localhost"
port = 1883         
 
client = mqttClient.Client()
client.on_connect= on_connect
client.on_message= on_message
 
client.connect(broker_address, port=port)
client.loop_start()
 
try:
    while True:
        time.sleep(1) 
except KeyboardInterrupt:
    print ("exiting")
    client.disconnect()
    client.loop_stop()
