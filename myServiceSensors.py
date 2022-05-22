import threading
import time
import json
import logging
import importlib.util
from logging.handlers import RotatingFileHandler
from configparser import ConfigParser



class thr_Sensor(threading.Thread):
    def __init__(self, chanel,update_rate, lib, config):
        threading.Thread.__init__(self)
        self.logger_prefix = "Sensor Thread - chanel:" + str(chanel) + " - "
        self.chanel = chanel
        self.update_rate = update_rate
        self.lib = lib
        self.config = config
        self.sensor_spec = importlib.util.spec_from_file_location("Sensor",lib)
        self.sensor = importlib.util.module_from_spec(self.sensor_spec)
        self.sensor_spec.loader.exec_module(self.sensor)
        self.sensor.Sensor.init(config)
    def run(self):
        logger.debug(self.logger_prefix+"Start Sensor")
        while True:
            if(self.sensor.Sensor.read()):
                while (len(self.sensor.Readings) != 0):
                    sens_time = self.sensor.Readings[0]['time']
                    sens_type = self.sensor.Readings[0]['Type']
                    sens_value =self.sensor.Readings[0]['value']
                    logger.debug(self.logger_prefix+ "Time :" + str(sens_time)+", Type:" + sens_type + ", Value:" + str(sens_value))
                    self.sensor.Readings.pop(0)
            else:
                #TODO: write into Database that the sensor isnt working on the 1st time
                #TODO: check Database if sensor is working again --> if sensor got changed and db got updated
                logger.warning(self.logger_prefix+ "Sensor not Working")
            time.sleep(self.update_rate)

#############################################
# load ini
#############################################
config = ConfigParser()
config.read('config.ini')
#Logging Config
cfg_logging_location = config.get('path','log_File')
cfg_path_sensor_home = config.get('path','sensor_lib_home')
cfg_logging_level_debug = config.getboolean('debug','log_debug')
cfg_logging_level_info = config.getboolean('debug','log_info')
cfg_logging_level_warnings = config.getboolean('debug','log_warnings')
#Load Sensors
cfg_JsonSensors = config.get('Sensors','json_Sensors')
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
formatter = logging.Formatter('%(asctime)s - %(name)s - myServiceSensors - %(levelname)s - %(message)s')  #
fh.setFormatter(formatter)                                                                              #
logger.addHandler(fh)  

#############################################
# INI config check
#############################################

running_sensor_threads = []
tmpObjects = json.loads(cfg_JsonSensors)
for x in tmpObjects:
    
    chanel = x['chanel']
    lib = x['lib']
    lib = cfg_path_sensor_home + lib
    update_rate = x['update_rate']
    config = x['config']
    logger.debug('Start Sensor Thread - Chanel:'+str(chanel)+", update_rate:"+str(update_rate)+"sec, using: " + lib + ", witch config:" + config)
    Sensor = thr_Sensor(chanel,update_rate,lib,config)
    running_sensor_threads.append(Sensor)
    Sensor.start()

for x in running_sensor_threads:
    x.join()