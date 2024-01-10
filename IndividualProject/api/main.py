from Flask import Flask, jsonify
import threading
import serial
import mysql.connector
from mysql.connector import Error


app = Flask(__name__)
@app.route('/api/v1/sensor-data', methods=['GET'])
def get_sensor_data():
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM SensorData ORDER BY id DESC LIMIT 10")
            records = cursor.fetchall()
            print("Total number of rows in SensorData is: ", cursor.rowcount)
            print("\nPrinting each SensorData record")
            
            data = []
            for row in records:
                data.append({
                    'DHTTemperature': row[1],
                    'Humidity': row[2],
                    'LM35Temperature': row[3],
                    'Time': row[4]
                })
            
            # Only keep the recent 200 data
            if len(data) > 200:
                data = data[-200:]
                
            return jsonify(data)
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)