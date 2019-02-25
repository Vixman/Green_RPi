import paho.mqtt.client as mqttClient
import time
 
def on_connect(client, userdata, flags, rc): 
    if rc == 0: 
        print("Connected to broker")
        global Connected            
        Connected = True                 
    else: 
        print("Connection failed")

 
def on_message(client, userdata, message):
    print "Current conditions: "  + message.payload

 
Connected = False
 
broker_address= "vixman"
port = 9001         
 
client = mqttClient.Client()
client.on_connect= on_connect
client.on_message= on_message
 
client.connect(broker_address, port=port)
client.loop_start()
 
while Connected != True:
    time.sleep(1)
 
client.subscribe("/sensors/dht22/")
 
try:
    while True:
        time.sleep(1) 
except KeyboardInterrupt:
    print "exiting"
    client.disconnect()
    client.loop_stop()
