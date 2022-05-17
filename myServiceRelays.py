import threading
import time
import logging
import relay_rasp
import sys
from logging.handlers import RotatingFileHandler
from configparser import ConfigParser

Relay_Situation = []
Relay_Situation_mutex = threading.Lock()
###################################################
#   Hardware Thread
#
#       checks if Relay_Situation has changed
#       and applys those changes to the Hardware

class thr_Relay_Hardware_controll(threading.Thread):
    def __init__(self, update_rate, pinout, Situation):
        threading.Thread.__init__(self)
        self.logger_prefix = "Hardware Controll Thread - "
        self.update_rate = update_rate
        self.count = len(pinout)
        self.pinout = pinout
        self.Situation = Situation.copy()
        self.hardware = relay_rasp.Relay(self.pinout, self.Situation)


    def run(self):
        logger.debug(self.logger_prefix+"Start Hardware Controll Thread")
        global Relay_Situation

        while True:
            Relay_Situation_mutex.acquire
            situation_changed = False
            logger.debug(self.logger_prefix+"Check for Change" + str(self.Situation) + str(Relay_Situation))
            for i in range(0,self.count,1):
                if(int(self.Situation[i]) != int(Relay_Situation[i])):
                    situation_changed = True
            if (situation_changed):
                self.Situation = Relay_Situation.copy()
                logger.debug(self.logger_prefix+"Situation has changed from "+str(Relay_Situation)+" to "+str(self.Situation))
                self.apply_Situation_to_Relays()
            Relay_Situation_mutex.release
            time.sleep(self.update_rate)
    
    def apply_Situation_to_Relays(self):
        for i in range(0,self.count,1):
            if int(self.Situation[i]) != int(self.hardware.state[i]):
                if int(self.Situation[i]) == 1:
                    self.hardware.Switch_ON_Ch(i)
                else:
                    self.hardware.Switch_OFF_Ch(i)

class thr_Relay_Database_Rule_Check(threading.Thread):
    def __init__(self, update_rate):
        threading.Thread.__init__(self)
        self.logger_prefix = "Database Rule Check Thread - "
        self.update_rate = update_rate
    
    def run(self):
        logger.debug(self.logger_prefix+"Start Database Rule Check Thread")
        global Relay_Situation
        while True:
            time.sleep(self.update_rate*2)
            self.change_Relay_Situation()
            logger.debug(self.logger_prefix+"new situation " + str(Relay_Situation))
    
    def change_Relay_Situation(self):
        Relay_Situation_mutex.acquire
        i = -1
        for r in range(0,len(Relay_Situation),1):
            if Relay_Situation[r] == 1:
                i = r
        if i == -1:
            Relay_Situation[0] = 1
            i = 0
        elif i == len(Relay_Situation)-1:
            Relay_Situation[len(Relay_Situation)-1] = 0
            Relay_Situation[0] = 1
            i = 0
        else:
            Relay_Situation[i] = 0
            Relay_Situation[i+1] = 1
            i += 1
        Relay_Situation_mutex.release



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

####
if len(cfg_BCM_GPIO_Pinout) != len(cfg_relay_Situation):
    logger.warning("Config - \"activation_Situation\" and \"BCM-GPIO\" have unequal lenght")
    #TODO: cut Situation to fit BCM - Pinout or fill Situation up with switched off relays
#############################################
# Start Threads
#############################################
logger.debug('Starting Threads')
thread_hardware = thr_Relay_Hardware_controll(cfg_relay_update_rate, cfg_BCM_GPIO_Pinout, cfg_relay_Situation)
thread_database = thr_Relay_Database_Rule_Check(cfg_relay_update_rate)
thread_hardware.start()
thread_database.start()
thread_hardware.join()
thread_database.join()