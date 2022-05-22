import json
import datetime
from time import sleep
config = json.loads("{\"value\": 0.0}")
counter = 1
working = True
Readings = []

class Sensor():
    def init(json_config:'str') -> None:
        global config
        config = json.loads(json_config)

    
    def read() -> 'bool':
        # Sensor Action
        global counter
        global working
        now = getTimestamp()   # timestamp of sensor reading
        type = 'TEST'   # type of Reading
        value = config['value'] * counter  # using config data as mocking Sensor Value
        counter += 1
        addReading(now,type,value) # add Data to output
        return working


def addReading(time:'int',type:'str',value:'float'):
    global Readings
    # 'time'     as UTC timestamp
    # 'type'     as short string describing the Reading
    # 'value'    as float Value for the reading
    # 'jSon_Data' as String containing a json structure with the raw Data
    entry = {
        "time" : time,
        "Type" : type,
        "value" : value
    }
    Readings.append(entry)

def getTimestamp()-> int:
    now = datetime.datetime.now(datetime.timezone.utc)
    return int(now.timestamp())