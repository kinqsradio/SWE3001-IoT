from flask import Flask, jsonify, render_template
import mysql.connector
from mysql.connector import Error
from dbConfig import config


app = Flask(__name__)

@app.route('/api/v1/sensor-data', methods=['GET'])
def get_sensor_data():
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM SensorData ORDER BY id DESC LIMIT 10")
            records = cursor.fetchall()
            
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

@app.route('/', methods=['GET'])
def home():
    data = get_sensor_data()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
