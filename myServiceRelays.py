import threading
import time
import logging
import relay_rasp
import sys
from logging.handlers import RotatingFileHandler
from configparser import ConfigParser

Relay_Situation = []
Relay_Situation_mutex = threading.Lock()

class thr_Relay_Hardware_controll(threading.Thread):
    def __init__(self, count, pinout, Situation, update_rate):
        threading.Thread.__init__(self)
        self.logger_prefix = "Hardware Controll Thread - "
        self.count = count
        self.pinout = pinout
        self.Situation = Situation
        self.update_rate = update_rate
        self.hardware = relay_rasp.Relay(self.pinout, self.Situation)


    def run(self):
        logger.debug(self.logger_prefix+"Start Hardware Controll Thread")
        global Relay_Situation

        while True:
            Relay_Situation_mutex.acquire
            if (self.Situation != Relay_Situation):
                self.Situation = Relay_Situation
                logger.debug(self.logger_prefix+"Situation has changed from "+self.State+" to "+self.Situation)
                self.apply_Situation_to_Relays()
            Relay_Situation_mutex.release
            time.sleep(self.update_rate)
    
    def apply_Situation_to_Relays(self):
        for i in range(0,self.count,1):
            if self.Situation[i] != self.hardware.state[i]:
                if self.Situation[i] == 1:
                    logger.error(self.logger_prefix+" Switch Relay " + str(i) + " ON")
                    #self.hardware.Switch_ON_Ch(i)
                else:
                    logger.error(self.logger_prefix+" Switch Relay " + str(i) + " OFF")
                    #self.hardware.Switch_OFF_Ch(i)


def thread_database_rule_check():
    logger.debug("Start Relay Database Rules Thread")

def thread_json_rpc():
    logger.debug("Start Json RPC Thread")



#############################################
# load ini
#############################################
config = ConfigParser()
config.read('config.ini')
#Logging Config
cfg_logging_location = config.get('path','log_File')
cfg_logging_level_debug = config.getboolean('debug','log_debug')
cfg_logging_level_info = config.getboolean('debug','log_info')
cfg_logging_level_warnings = config.getboolean('debug','log_warnings')
#Relay Config
cfg_relay_count = config.getint('Relay','relay-count')  #relay count
cfg_BCM_GPIO_Pinout = config.get('Relay','BCM-GPIO')
cfg_BCM_GPIO_Pinout = cfg_BCM_GPIO_Pinout.replace('[', '')
cfg_BCM_GPIO_Pinout = cfg_BCM_GPIO_Pinout.replace(']', '')
cfg_BCM_GPIO_Pinout = cfg_BCM_GPIO_Pinout.split(',')    #array of BCM Pins as Integer
for i in range(0,len(cfg_BCM_GPIO_Pinout)):
    cfg_BCM_GPIO_Pinout[i] = int(cfg_BCM_GPIO_Pinout[i])
cfg_relay_Situation = config.get('Relay','activation_Situation')
cfg_relay_Situation = cfg_relay_Situation.replace('[', '')
cfg_relay_Situation = cfg_relay_Situation.replace(']', '')
cfg_relay_Situation = cfg_relay_Situation.split(',')    #array of Relay Situations as Integer
for i in range(0,len(cfg_relay_Situation)):
    cfg_relay_Situation[i] = int(cfg_relay_Situation[i])
Relay_Situation = cfg_relay_Situation
cfg_relay_update_rate = config.getfloat('Relay','Updata-rate_in-sec')
#############################################
# Logger init
#############################################
# LEVEL    Numeric Value
#----------
# CRITICAL  50
# ERROR     40
# WARNING   30
# INFO      20
# DEBUG     10
logger = logging.getLogger("_SeRAPiS_")
if cfg_logging_level_debug:
    logger.setLevel(logging.DEBUG)
else:
    if cfg_logging_level_info:
        logger.setLevel(logging.INFO)
    else:
        if cfg_logging_level_warnings:
            logger.setLevel(logging.WARNING)
        else:
            logger.setLevel(logging.ERROR)
fh = RotatingFileHandler(cfg_logging_location, maxBytes=2000000, backupCount=10)                        #
formatter = logging.Formatter('%(asctime)s - %(name)s - myServiceRelay - %(levelname)s - %(message)s')  #
fh.setFormatter(formatter)                                                                              #
logger.addHandler(fh)  


#############################################
# Start Threads
#############################################
logger.debug('Starting Threads')
thread_hardware = thr_Relay_Hardware_controll(cfg_relay_count, cfg_BCM_GPIO_Pinout, cfg_relay_Situation, cfg_relay_update_rate)
thread_hardware.start()
thread_hardware.join()