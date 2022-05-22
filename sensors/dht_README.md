# DHT
reads dht sensor
## Install
````#sudo pip3 install Adafruit_DHT```` 

## Constructor
```
json_config as String structure
    {
        "Sensor": int Sensor Value
        "BCM-GPIO": BCM pin as int
    }
```
| Sensor | Value |
|---|---|
| DHT 11 | 11 |
| DHT 22 | 22 |
| AM2302 | 2302 |

## read()
reads sensor and stores results in Readings[]
### Readings[]
array of 

| type | description |
|---|---|
| "temp" | Temperature |
| "rel_humid" | relative-humidity |