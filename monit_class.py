import Adafruit_DHT
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError
import paho.mqtt.client as mqtt
import json

class Monit():
    def __init__(self):
        #Thread.__init__(self)
        self.sensor = Adafruit_DHT.DHT11
        self.pin = 4
        self.reads = Adafruit_DHT.read_retry(self.sensor, self.pin)
        self.temp = None
        self.humidity = None
        self.client = InfluxDBClient(hostname, port, user,
                                     passwd, dbname)
        
    def get_temp(self):    
        self.temp = self.reads[1]
        return self.temp

    def get_hum(self):
        self.hum = self.reads[0]
        return self.hum

    def dbcon(self):
        while True:
            
            json_body = [
            {
                "measurement": "temperature",
                "tags": {
                    "location": "home rpi",
                    "region": "Wro-PL"
                },
                "time": datetime.today(),
                "fields":{
                    "value": str(self.get_temp())
                }
            }
        ]


            json_body1 = [
            {
                "measurement": "hum",
                "tags": {
                    "location": "home rpi",
                    "region": "Wro-PL"
                },
                "time": datetime.today(),
                "fields":{
                    "value": str(self.get_hum())
                }
            }
        ]        

            self.client.write_points(json_body)
            self.client.write_points(json_body1)
            result = self.client.query('select value from hum;')
            #print result
            time.sleep(60)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code {}".format(rc))

client = mqtt.Client()
client.on_connect = on_connect
client.connect(hostname, port, timeout)
client.loop_start()

try:
    while True:
        mon = Monit() 
        mon.dbcon()
        dht22_data = {'temperature': 0, 'humidity': 0}
        dht22_data[temperature] = mon.get_temp()
        dht22_data[humidity] = mon.get_hum()
        clinet.publish('/sensors/dht22/', json.dumps(dht22_data), 2)
except KeyboardInterrupt:
    pass
