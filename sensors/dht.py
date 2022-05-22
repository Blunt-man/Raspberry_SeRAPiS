import json
import datetime
import Adafruit_DHT #sudo pip3 install Adafruit_DHT

config = json.loads("{\"Sensor\": 11, \"BCM-GPIO\": 4}")
used_Sensor = Adafruit_DHT.DHT11
working = True
Readings = []

class Sensor():

    def init(json_config:'str') -> None:
        global config
        global used_Sensor
        global working
        config = json.loads(json_config)
        # {"Sensor": x, "BCM-GPIO": y}
        #     x  		Sensor Name
        #     11        Adafruit_HDT.DHT11
        #     22        Adafruit_HDT.DHT22
        #     2302      Adafruit_HDT.AM2302
        if(int(config['Sensor']) == 11):
            used_Sensor = Adafruit_DHT.DHT11
        elif(int(config['Sensor']) == 22):
            used_Sensor = Adafruit_DHT.DHT22
        elif(int(config['Sensor']) == 2302):
            used_Sensor = Adafruit_DHT.AM2302
        else:
            working = False
        

    
    def read() -> 'bool':
        global working
        if working:
            now = getTimestamp()
            humidity, temperature = Adafruit_DHT.read_retry(used_Sensor, int(config['BCM-GPIO']))
            #find out if Sensor is still working .... result should be float
            if (type(humidity) != type(0.0)):
                working = False
            else:
                addReading(now,"temp",temperature)
                addReading(now,"rel_humid", humidity)
        return working

def getTimestamp()-> int:
    now = datetime.datetime.now(datetime.timezone.utc)
    return int(now.timestamp())

def addReading(time:'int',type:'str',value:'float'):
    global Readings
    entry = {
        "time" : time,
        "Type" : type,
        "value" : value
    }
    Readings.append(entry)