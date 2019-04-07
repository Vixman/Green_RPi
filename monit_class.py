import Adafruit_DHT
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError
import paho.mqtt.client as mqtt
import json
import time

class Monit():
    def __init__(self):
        #Thread.__init__(self)
        self.sensor = Adafruit_DHT.DHT11
        self.pin = 4
        self.reads = Adafruit_DHT.read_retry(self.sensor, self.pin)
        self.temp = None
        self.humidity = None
        
    def get_temp(self):    
        self.temp = self.reads[1]
        return self.temp

    def get_hum(self):
        self.hum = self.reads[0]
        return self.hum


def on_connect(client, userdata, flags, rc):
    if rc == 0: 
        print("Connected to broker")
        global Connected            
        Connected = True                 
    else: 
        print("Connection failed")

client = mqtt.Client()
client.on_connect = on_connect
client.connect("localhost", 1883, 71)
client.loop_start()

try:
    while True:
        mon = Monit() 
        #mon.dbcon()
        dht22_data = {'temperature': 0, 'humidity': 0}
        dht22_data['temperature'] = mon.get_temp()
        dht22_data['humidity'] = mon.get_hum()
        client.publish('/sensors/dht22/', json.dumps(dht22_data), 2)
        print (mon.get_temp())
        print (mon.get_hum())
        print (type(dht22_data))
        time.sleep(10)        
except KeyboardInterrupt:
    print ("exiting")
    client.disconnect()
    client.loop_stop()
