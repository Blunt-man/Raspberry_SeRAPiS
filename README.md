# Raspberry_SeRAPiS
Sensor Relay Action Pi System

```Python
home_dir
├── sensors
│   ├── _example_sensor_README.md
│   ├── _example_sensor.py
│   ├── dht_README.md
│   └── dht.py
│
├── myServiceDisplay.py
├── myServiceRelays.py
├── myServiceSensors.py
│
├── config.ini
├── database.py
├── relay_rasp.py
```
## Install
### Using Debian "wheezy" (5.10.103-v7+) on Raspberry Pi 3 Model B
Install python 3
```console
$sudo apt update
$sudo apt upgrade
$sudo apt-get install python3 python3-pip 
```

allow remote client connection on MariaDB (remember to allow both ipv4 and ipv6)
```console
$sudo mysql db_name
SELECT User, Host FROM mysql.user WHERE Host <> 'localhost';
GRANT ALL PRIVILEGES ON *.* TO 'user'@'adress' IDENTIFIED BY 'password' WITH GRANT OPTION;
```
## Info
---
one or more Raspberry Pis
<ul>
    <li>Collecting Sensor Data</li>
    <li>Controlling Relays</li>
    <li>Displaying Data</li>
</ul>
<br />


### Relays
myServiceRelays.py ***- unfinished*** 
<br /> runns as systemD Process
<br /> controlls the Relys...

---
### Sensors

[_example_sensor](sensors/_example_sensor_README.md)<br />
[dht](sensors/dht_README.md)

#### myServiceSensors.py ***- unfinished***
<br /> runns as systemD Process
<br /> starts a Thread per configured Sensor
<br /> new Sensor librarys can be added into the config.ini file

---
#### Sensor library
a Sensor library has
<br /> gets a json string with its configuration (from the config.ini)
<br /> returns an array 'double' representing the Value of the mesurement and a corresponding string representing the type
<br /> and a json Structure with the raw Data (if a Sensor library)

---
---
## Hardware
### Raspberry Pi GPIO Example Pin map
Situation with 
<ul>
        <li>8 Relays</li>
        <li>2 DHT22 Sensors</li>
        <li>ePaper Display</li>
</ul>

| Info | BCM | wPi | Name | Mode | V | Physical | Physical | V | Mode | Name | wPi | BCM | Info |
|:---|---:|---:|---:|---:|:---:|---:|:---|:---:|:---|:---|:---|---:|---:|
|DHT 22 | | | 3.3v | | | 1 | 2 | | | 5v | | | |           
| | 2 | 8 | SDA.1 | IN | 1 | 3 | 4 | | | 5v | | | |
| | 3 | 9 | SCL.1 | IN | 1 | 5 | 6 | | | 0v | | | |
| DHT 22 | 4 | 7 | GPIO. 7 | IN | 1 | 7 | 8 | 1 | ALT5 | TxD | 15 | 14 | UART->Pico |
| | | | 0v | | | 9 | 10 | 1 | IN | RxD | 16 | 15 | Pico->UART |
| ePaper | 17 | 0 | GPIO. 0 | OUT | 0 | 11 | 12 | 0 | IN | GPIO. 1 | 1 | 18 | |
| | 27 | 2 | GPIO. 2 | OUT | 0 | 13 | 14 | | | 0v | | | |
| | 22 | 3 | GPIO. 3 | IN | 0 | 15 | 16 | 0 | IN | GPIO. 4 | 4 | 23 | |
| ePaper | | | 3.3v | | | 17 | 18 | 0 | IN | GPIO. 5 | 5 | 24 | ePaper |
| ePaper | 10 | 12 | MOSI | ALT0 | 0 | 19 | 20 | | | 0v | | | |
| | 9 | 13 | MISO | ALT0 | 0 | 21 | 22 | 0 | OUT  | GPIO. 6 | 6 | 25 | ePaper |
| ePaper | 11 | 14 | SCLK | ALT0 | 0 | 23 | 24 | 1 | OUT | CE0 | 10 | 8 | ePaper |
| | | | 0v | | | 25 | 26 | 1 | OUT | CE1 | 11 | 7 | |
| | 0 | 30 | SDA.0 | IN | 1 | 27 | 28 | 1 | IN | SCL.0 | 31 | 1 | |
| Relay CH 1 | 5 | 21 | GPIO.21 | OUT | 1 | 29 | 30 | | | 0v | | | |
| Relay CH 2 | 6 | 22 | GPIO.22 | OUT | 1 | 31 | 32 | 0 | OUT  | GPIO.26 | 26 | 12 | dht22 2 |
| Relay CH 3 | 13 | 23 | GPIO.23 | OUT | 0 | 33 | 34 | | | 0v | | | |
| Relay CH 5 | 19 | 24 | GPIO.24 | OUT | 1 | 35 | 36 | 1 | OUT | GPIO.27 | 27 | 16 | Relay CH 4 |
| Relay CH 8 | 26 | 25 | GPIO.25 | OUT | 0 | 37 | 38 | 0 | OUT | GPIO.28 | 28 | 20 | Relay CH 6 |
| | | | 0v | | | 39 | 40 | 0 | OUT | GPIO.29 | 29 | 21 | Relay CH 7 |


<img src="nfo/example_setup-rpi.svg">
---
---
## Database Layout
using MariaDB
### Tables


#### Box
| ID | Name | Host | Relay_Ch_Names | Relay_Routine_id | Relay_logging |
|---|---|---|---|---|---|
| *int* | *string* | *string* | *string* | *int* | *Bool* |
|-|-|-|-|-|-|
|---|Box Name|network Address|Relay_chanel description|---|---|

#### Relay_Routine
| ID | Relay_Count | Name | UTC_update |
|---|---|---|---|
| *int* | *int*| *string* | *int* |

 <br /> <br />
'Relay_settings' describes a Rule <br />each Symbol Representing a Relay separate by '|' <br /> Symbols are:

|||
|--|--|
|1| Relay gets Switched ON, if rule applys|
|0| Relay gets Switched OFF, if rule applys|
|#| Relay State will be ignored i.e. stays the same if rule applys|
|+| Relay State has to be switched ON otherwise rule will be ignored|
|-| Relay State has to be switched OFF otherwise rule will be ignored|
||


#### Relay_Routine_day
| ID | Relay_Routine_id | daily_offset_sec | Relay_seting | info |
|---|---|---|---|---|
|*int* | *int* | *int* | *string* | *string* |
|-|-|-|-|-|
|||3600|0\|0\|0\|0|Example: <br />every Day at 1:00:00 UTC <br />all 4 Relays get switched OFF|
|||46800|1\|#\|+\|0|Example: <br />every Day at 13:00:00 UTC <br />if the 3rd Relay is Switched on <br />switch on 1st Relay <br /> adopt state of 2nd Relay <br />switch off 4th Relay

#### Relay_Routine_hour
| ID | Relay_Routine_id | hourly_offset_sec | Relay_seting | info |
|---|---|---|---|---|
|*int* | *int* | *int* | *string* | *string* |
|-|-|-|-|-|

#### Relay_Special_Event
| ID | Box_id | UTC_Event | Relay_seting | info |
|---|---|---|---|---|
| *int* | *int* | *int* | *string* | *string* |
|-|-|-|-|-|
|||1652802500|1\|#\|#\|#|on the 17. Mai 2022 at 15:48:20<br />Switch ON 1st Relay<br/>apodt the State of the other 3 Relays

#### Relay_Sensor Rules
| ID | Relay_Routine_id |
|---|---|
| *int* | *int* |
|-|-|
|||

#### Sensors
| ID | Box_ID | Chanel | Working | utilisation_counter | fst_use_UTC | Sensor_Type | info |
|---|---|---|---|---|---|---|---|
| *int* | *int* | *int* | *Bool* | *int* | *int* | *string* | *string* |
|-|-|-|-|-|-|-|-|
| - | - |1|True|1|1652802500|DHT22|DHT22 returning relative humidity and temperature|

#### timeline_Sensor
| ID | Sensor_ID | UTC | Type | Value |
|---|---|---|---|---|
| *int* | *int* | *int* | *string* | *double* |
|-|-|-|-|-|
| - | 1 | 1652802500 | temp | 22.4 |
| - | 1 | 1652802500 | rel_humid | 52.6 |

#### timeline_Relays
| ID | Box_ID | UTC | Situation |
|---|---|---|---|
| *int* | *int* | *int* | *string* |
|-|-|-|-|
||1|1652802500|0\|0\|0\|0|
||1|1652803000|1\|0\|0\|0|
