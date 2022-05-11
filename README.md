# Raspberry_SeRAPiS

## Info

## Hardware
  Raspberry Pi GPIO Pin map                                                                         
  
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
|  |  |  | 0v |  |  | 39 | 40 | 0 | OUT | GPIO.29 | 29 | 21 | Relay CH 7 |