from flask import Flask, jsonify, render_template
import threading
import serial
import mysql.connector
from mysql.connector import Error
import datetime
import time
from dbConfig import config

app = Flask(__name__)

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

def read_sensor_data():
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            cursor = connection.cursor()
            create_database(cursor, 'Arduino')
            connection.database = 'Arduino'
            create_table(cursor, 'SensorData')

            ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
            ser.flush()
            last_recorded_time = 0

            while True:
                current_time = time.time()
                if current_time - last_recorded_time >= 60:  # 60 seconds = 1 minute
                    if ser.in_waiting > 0:
                        line = ser.readline().decode('utf-8').rstrip()
                        parts = line.split(',')
                        if len(parts) == 3:
                            try:
                                dht_temp = float(parts[0])
                                humidity = float(parts[1])
                                lm35_temp = float(parts[2])
                                current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                mySql_insert_query = """INSERT INTO SensorData (DHTTemperature, Humidity, LM35Temperature, Time) 
                                                        VALUES (%s, %s, %s, %s) """
                                record = (dht_temp, humidity, lm35_temp, current_datetime)
                                cursor.execute(mySql_insert_query, record)
                                connection.commit()
                                print("Record inserted successfully into SensorData table")
                                last_recorded_time = current_time
                            except ValueError as e:
                                print(f"Error parsing data: {e}")
                                continue
                        else:
                            print("Incomplete data received")
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

@app.route('/api/v1/sensor-data', methods=['GET'])
def get_sensor_data():
    data = []
    try:
        connection = mysql.connector.connect(**config)
        connection.database = 'Arduino' # Select database
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM SensorData ORDER BY id DESC LIMIT 60")
            records = cursor.fetchall()
            for row in records:
                data.append({
                    'DHTTemperature': row[1],
                    'Humidity': row[2],
                    'LM35Temperature': row[3],
                    'Time': row[4].strftime('%Y-%m-%d %H:%M:%S') if row[4] else None
                })
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return jsonify(data)

@app.route('/', methods=['GET'])
def home():
    data = get_sensor_data().get_json()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    sensor_thread = threading.Thread(target=get_sensor_data().get_json(), daemon=True)
    sensor_thread.start()
    app.run(host='192.168.2.4', port=8080)
