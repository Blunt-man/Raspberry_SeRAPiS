import mariadb 
#pip3 install mariadb
#sudo apt-get install libmariadb3
from configparser import ConfigParser
import socket
import time
dbuser = ""
dbpassword = ""
dbhost = ""
dbport = 0
dbdatabase = ""
class DB_Sensor():
    def __init__(self, Sensor_Chanel):
        #load_ini()
        self.Sensor_Chanel = Sensor_Chanel

        host = get_Host_name()
        conn = get_db_connection()

        cur = conn.cursor()
        self.Box_ID = get_Box_ID_with_Hostname(cur, host)

        cur.execute(f"SELECT id, Sensor_Typ, utilisation_Counter, Working FROM Sensor WHERE Box_id = {self.Box_ID} and Sensor_ch = {self.Sensor_Chanel};")
        
        row = cur.fetchone()

        self.ID = row[0]
        self.Typ = row[1]
        self.utilisation_counter = row[2]
        self.working = bool(row[3])
        conn.close()
    
    def utilise_Sensor(self):
        self.utilisation_counter = self.utilisation_counter + 1
        conn = get_db_connection()
        cur = conn.cursor()
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



def get_db_connection():
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

def load_connection_from_ini():
    config = ConfigParser()
    config.read('config.ini')
    global dbuser
    global dbpassword
    global dbhost
    global dbport
    global dbdatabase
    dbuser = config.get('database','user')
    dbpassword = config.get('database','password')
    dbhost = config.get('database','host')
    dbport = config.getint('database','port')
    dbdatabase = config.get('database','database')

def get_Host_name():                    # return String with localhost Name using socket
    try:
        return socket.gethostname()
    except:
        print("Unable to get Hostname") #TODO log error

def get_Box_ID_with_Hostname(cur, host) -> int:                 # get Database Box_id       based on Hostname
    cur.execute(f"SELECT id FROM Box WHERE Host='{host}'")
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
