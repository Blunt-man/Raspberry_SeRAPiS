# _example_sensor.py
represents the template for Sensor implemenattions
## Constructor
```Python
#example
    json_config = "{\"Sensor\": 11, \"BCM-GPIO\": 27}"
```
```Python
class Sensor():
    def init(json_config:'str') -> None:
        global config
        config = json.loads(json_config)
    def read() -> 'bool':
        # Sensor Action
        global working

        now = getTimestamp()
        value =
        #reading sensor Data
        
        #storing data of a Type
        addReading(now,type,value)


        return working
```

## Execute Sensor Reading

```Python
Sensor.read() -> bool
```
reads Data
stores results in Readings[] list<br />
returns if Sensor is working
```Python
getTimestamp(self) -> int
```
return timestamp now as integer

## Results
```Python
Sensor.addReading(self,time:'int',type:'str',value:'float'):
```
adds an entry to Readings[] list <br />
type should be a short string describing the Sensor Data
```Python 
Sensor.Reading[{
    "time" : int,
    "Type" : str,
    "value" : float
},...]
```
# Example

for example a DHT22 has 2 results (the relative humidity and temperature)

```Python
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
```