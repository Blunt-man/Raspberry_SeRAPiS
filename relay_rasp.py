import RPi.GPIO as GPIO         #sudo apt install python3-rpi.gpio
import traceback
import logging
logging_prefix = "[relay_rasp.py] - "
class Relay():
    def __init__(self, pinout, state):
        self.pinout = pinout
        self.state = state.copy()
        self.logger = logging.getLogger("_SeRAPiS_")
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        #initialise every used GPIO Port
        # and set output State accord to the set Situation
        try:
            for r in range(0,len(self.pinout),1):
                GPIO.setup(self.pinout[r],GPIO.OUT)
                if self.state[r] == 0:
                    self.logger.debug(logging_prefix + "init - Switch off  Relay Chanel: "+str(r)+" on Pin " + str(self.pinout[r]))
                    GPIO.output(self.pinout[r],GPIO.HIGH)
                else:
                    self.logger.debug(logging_prefix + "init - Switch on  Relay Chanel: "+str(r)+" on Pin " + str(self.pinout[r]))
                    GPIO.output(self.pinout[r],GPIO.LOW)
        except:
            self.logger.error(logging_prefix + 'Initialisation BCM Pinout',traceback.format_exc())
   
    def Switch_ON_Ch(self, Chanel):
        try:
            if Chanel <= len(self.pinout)-1 and Chanel >= 0:
                GPIO.output(self.pinout[Chanel],GPIO.LOW)
                self.state[Chanel] = 1
                self.logger.debug(logging_prefix + "Switch_ON_Ch: "+str(Chanel)+" on Pin " + str(self.pinout[Chanel]))
        except:
            self.logger.error(logging_prefix + 'Switch_ON_Ch ',traceback.format_exc())
    
    def Switch_OFF_Ch(self, Chanel):
        try:
            if Chanel <= len(self.pinout)-1 and Chanel >= 0:
                GPIO.output(self.pinout[Chanel],GPIO.HIGH)
                self.state[Chanel] = 0
                self.logger.debug(logging_prefix + "Switch_OFF_Ch: " + str(Chanel)+ " on Pin "+str(self.pinout[Chanel]))
        except:
            self.logger.error(logging_prefix + 'Switch_OFF_Ch ',traceback.format_exc())