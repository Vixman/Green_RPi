import Adafruit_DHT
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError


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
            print result
            time.sleep(20)


mon = Monit() 
mon.dbcon()
