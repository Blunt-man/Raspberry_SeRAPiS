import RPi.GPIO as GPIO         #sudo apt install python3-rpi.gpio
import traceback
import logging
#TODO: Fix logging
class Relay():
    def __init__(self, pinout, state):
        self.pinout = pinout
        self.state = state
        self.logger = logging.getLogger("_SeRAPiS_")
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        #initialise every used GPIO Port
        # and set output State accord to the set Situation
        try:
            for r in range(0,len(self.pinout),1):
                print(self.pinout[r])
                GPIO.setup(self.pinout[r],GPIO.OUT)
                if self.state[r] == 0:
                    self.logger.debug("relay_rasp.py - init - Switch off  Relay Chanel: "+str(r)+" on Pin " + str(self.pinout[r]))
                    GPIO.output(self.pinout[r],GPIO.HIGH)
                else:
                    self.logger.debug("relay_rasp.py - init - Switch on  Relay Chanel: "+str(r)+" on Pin " + str(self.pinout[r]))
                    GPIO.output(self.pinout[r],GPIO.LOW)
        except:
            self.logger.error('relay_rasp.py - Initialisation BCM Pinout',traceback.format_exc())
   
    def Switch_ON_Ch(self, Chanel):
        try:
            if Chanel <= len(self.pinout)-1 and Chanel >= 0:
                GPIO.output(self.pinout[Chanel],GPIO.LOW)
                self.logger.debug("relay_rasp.py - Switch on  Relay Chanel: "+str(Relay)+" on Pin " + str(self.pinout[Chanel]))
        except:
            self.logger.error('relay_rasp.py - SWITCH_ON Relay ',traceback.format_exc())
    
    def Switch_OFF_Ch(self, Chanel):
        try:
            if Chanel <= len(self.pinout)-1 and Chanel >= 0:
                GPIO.output(self.pinout[Chanel],GPIO.HIGH)
                self.logger.debug("relay_rasp.py - Switch off Relay Chanel: " + str(Relay)+ " on Pin "+str(self.pinout[Chanel]))
        except:
            self.logger.error('relay_rasp.py - SWITCH_OFF Relay ',traceback.format_exc())