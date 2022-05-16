import mariadb
from configparser import ConfigParser
import socket
dbuser = ""
dbpassword = ""
dbhost = ""
dbport = 0
dbdatabase = ""

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

def db_get_Box_ID_with_Hostname(cur, host):                 # get Database Box_id       based on Hostname
    cur.execute(f"SELECT id FROM Box WHERE Host='{host}'")
    return cur.fetchone()[0]

config = ConfigParser()
config.read('config.ini')

dbuser = config.get('database','user')
dbpassword = config.get('database','password')
dbhost = config.get('database','host')
dbport = config.getint('database','port')
dbdatabase = config.get('database','database')




load_connection_from_ini()
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

cur = conn.cursor()                     # get Cursor

localhost = get_Host_name()             # get Hostname
db_Box_id = db_get_Box_ID_with_Hostname(cur, localhost)

print ( db_Box_id)