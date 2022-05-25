import datetime
import logging
from xmlrpc.client import Boolean
import mariadb 
#pip3 install mariadb
#sudo apt-get install libmariadb3
from configparser import ConfigParser
import socket
dbuser = ""
dbpassword = ""
dbhost = ""
dbport = 0
dbdatabase = ""
Box_ID = 0

#TODO: implement logger

class DB_Sensor():
    def __init__(self, Sensor_Chanel):
        self.logger = logging.getLogger("_SeRAPiS_")
        self.Sensor_Chanel = Sensor_Chanel
        self.logger_prefix = " Database - Sensor-Chanel:" + str(Sensor_Chanel) + " - "
        #global Box_ID
        #load_ini()

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT id, Sensor_Typ, utilisation_Counter, Working FROM Sensor WHERE Box_id = {Box_ID} and Sensor_ch = {self.Sensor_Chanel};")
        #TODO: only load Working sensor.. if no working sensor for this box on this chanel exists 
        row = cur.fetchone()
        self.ID = row[0]
        self.Typ = row[1]
        self.utilisation_counter = row[2]
        self.working = bool(row[3])
        conn.close()
    
    def utilise_Sensor(self):
        conn = get_db_connection()
        cur = conn.cursor()
        if (int(self.utilisation_counter) <= 0):    #Sensor gets used for the 1st time
            now = getTimestamp()
            cur.execute(f"UPDATE Sensor SET UTC_1st_use = {now} WHERE ID = {self.ID}")
            conn.commit()
        self.utilisation_counter = self.utilisation_counter + 1
        cur.execute(f"UPDATE Sensor SET utilisation_Counter = {self.utilisation_counter} WHERE ID = {self.ID}")
        conn.commit()
        conn.close()
    
    def add_Sensor_timeline(self, time, type, value):
        conn = get_db_connection()
        cur = conn.cursor()
        #print(f"INSERT INTO timeline_Sensor (Sensor_id, UTC, Type, Value) VALUES ({self.ID},{time},\"{type}\",{value})")
        cur.execute(f"INSERT INTO timeline_Sensor (Sensor_id, UTC, Type, Value) VALUES ({self.ID},{time},\"{type}\",{value})")
        conn.commit()
        conn.close()

class DB_Relay():
    def __init__(self):
        self.logger = logging.getLogger("_SeRAPiS_")
        self.logger_prefix = ""
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT Relay_Routine_id FROM Box WHERE id = {Box_ID}")
        self.Routine_ID = cur.fetchone()[0]
        cur.execute(f"SELECT Situation_Start_of_Day FROM Relay_Routine WHERE id = {self.Routine_ID}")
        self.Situation = cur.fetchone()[0]
        self.Situation = self.Situation.split('|')
        for x in self.Situation:
            x = int(x)
        self.Routine_ID = 0
        self.latest_Routine_change = 0
        conn.close()
        self.Rules_Routine_day = []  #{"time":<datetime.timedelta>,"Rule":['+','-','#','1','0',...]}
        self.Rules_Routine_day__last_applyed = -1
        self.Rules_Routine_Sensors = []
        self.Rules_Special_Event = []
        self.Update_Routine()

    def Update_Routine(self):
        #checks if different Routine was selected in Database
        #                 or UTC_Routine_Update has changed i.e. the Rules of the selected Routine have changed
        # and loads the Routine from the Database
        def load_Routine():
            # reloads the full day of rules and the sensor rules [everything identified by the Relay_Routine[Relay_Routine_id]]
            def update_Rules_full_day():
                conn = get_db_connection()
                cur = conn.cursor()
                self.Rules_Routine_day = []
                cur.execute(f"SELECT daily_offset_sec, Relay_setting FROM Relay_Routine_day Where Relay_Routine_id={self.Routine_ID} ORDER BY daily_offset_sec ASC")
                for (daily_offset_sec, Relay_setting) in cur:
                    Rule = {
                        "time": datetime.timedelta(seconds = daily_offset_sec),
                        "Rule": Relay_setting.split('|')
                    }
                    self.Rules_Routine_day.append(Rule)
                
                cur.execute(f"SELECT hourly_offset_sec, Relay_setting FROM Relay_Routine_hour Where Relay_Routine_id={self.Routine_ID} ORDER BY hourly_offset_sec ASC")
                for (hourly_offset_sec, Relay_setting) in cur:
                    for x in range(24):
                        Rule = {
                            "time": datetime.timedelta(seconds = (60*60*x)+hourly_offset_sec),
                            "Rule": Relay_setting.split('|')
                        }
                        self.Rules_Routine_day.append(Rule)

                self.Rules_Routine_day = sorted(self.Rules_Routine_day, key=lambda x : x['time'], reverse=False)
                conn.close()
            def update_Rules_Sensors():
                self.Rules_Routine_Sensors = []
                #TODO:Load Sensor Rules From db
            def update_last_Routine_Change():
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute(f"SELECT UTC_Routine_Update FROM Relay_Routine WHERE id = {self.Routine_ID}")
                self.latest_Routine_change = cur.fetchone()[0]
                conn.close()
            def get_std_stiuation():
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute(f"SELECT Situation_Start_of_Day FROM Relay_Routine WHERE id = {self.Routine_ID}")
                self.Situation = cur.fetchone()[0]
                self.Situation = self.Situation.split('|')
                for x in self.Situation:
                    x = int(x)
                conn.close()
            update_Rules_full_day()
            update_Rules_Sensors()
            get_std_stiuation()
            update_last_Routine_Change()
        routine_changed = False
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT Relay_Routine_id FROM Box WHERE id = {Box_ID}")
        tmp_Routine_ID = cur.fetchone()[0]
        if self.Routine_ID != tmp_Routine_ID:
            #Routine has changed
            self.Routine_ID = tmp_Routine_ID
            routine_changed = True
        
        cur.execute(f"SELECT UTC_Routine_Update FROM Relay_Routine WHERE id = {self.Routine_ID}")
        tmp_time_Routine_update = cur.fetchone()[0]
        if self.latest_Routine_change != tmp_time_Routine_update:
            #Routine has changed
            routine_changed = True
        if routine_changed:
            load_Routine()
        conn.close()
    
    def load_special_events(self):
        #TODO: load Special Events from Database
        print()

    def logger_Relay_Situation(self, time, situation):
        #TODO: logging Relay Situation in Database if aktive
        print()
    



def init() -> Boolean:
    global Box_ID
    def get_Host_name() -> str:                    # return String with localhost Name using socket
        try:
            return socket.gethostname()
        except:
            print("Unable to get Hostname") #TODO log error

    def get_Box_ID_with_Hostname(cur, host) -> int:                 # get Database Box_id       based on Hostname
        cur.execute(f"SELECT id FROM Box WHERE Host='{host}'")
        #TODO: if Box_ID doesn't exist :
        #   -Add Box to DB
        return cur.fetchone()[0]
    
    def load_ini():
        global dbuser
        global dbpassword
        global dbhost
        global dbport
        global dbdatabase
        config = ConfigParser()
        config.read('config.ini')

        dbuser = config.get('database','user')
        dbpassword = config.get('database','password')
        dbhost = config.get('database','host')
        dbport = config.getint('database','port')
        dbdatabase = config.get('database','database')  

    hostname = get_Host_name()
    load_ini()
    con = get_db_connection()
    Box_ID = get_Box_ID_with_Hostname(con.cursor(),hostname)
    con.close()
    return True

def get_db_connection() -> mariadb.connect:
    try:
        conn = mariadb.connect(
            user=dbuser,
            password=dbpassword,
            host=dbhost,
            port=dbport,
            database=dbdatabase
        )
    except mariadb.Error as e:
        print('Error connecting to MariaDB Platform:', e)
    return conn

def getTimestamp()-> int:
    now = datetime.datetime.now(datetime.timezone.utc)
    return int(now.timestamp())