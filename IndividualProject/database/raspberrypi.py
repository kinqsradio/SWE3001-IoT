import serial
import mysql.connector
from mysql.connector import Error
import datetime
import time
from dbConfig import config

def create_database(cursor, db_name):
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
        print(f"Database '{db_name}' created or already exists.")
    except Error as e:
        print(f"Error creating database {db_name}: {e}")

def create_table(cursor, table_name):
    try:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                DHTTemperature FLOAT,
                Humidity FLOAT,
                LM35Temperature FLOAT,
                Time DATETIME
            );
        """)
        print(f"Table '{table_name}' created or already exists.")
    except Error as e:
        print(f"Error creating table {table_name}: {e}")

# Connect to MySQL Server (without specifying database)
try:
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        cursor = connection.cursor()
        # Create database if it doesn't exist
        create_database(cursor, 'Arduino')
        
        # Now connect to the database
        connection.database = 'Arduino'

        # Create table if it doesn't exist
        create_table(cursor, 'SensorData')

        # Setup serial connection
        ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
        ser.flush()

        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                # Assuming the line format is "DHT Temp: [temp], Humidity: [humidity]%, LM35 Temp: [temp]"
                parts = line.split(',')
                dht_temp = parts[0].split(':')[1].strip()
                humidity = parts[1].split(':')[1].strip('%').strip()
                lm35_temp = parts[2].split(':')[1].strip('°C').strip()
                
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Inserting data into table
                mySql_insert_query = """INSERT INTO SensorData (DHTTemperature, Humidity, LM35Temperature, Time) 
                                        VALUES (%s, %s, %s, %s) """
                record = (dht_temp, humidity, lm35_temp, current_time)
                cursor.execute(mySql_insert_query, record)
                connection.commit()
                print("Record inserted successfully into SensorData table")

except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
