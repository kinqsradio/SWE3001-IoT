from flask import Flask, jsonify, render_template
import mysql.connector
from mysql.connector import Error
from dbConfig import config


app = Flask(__name__)

@app.route('/api/v1/sensor-data', methods=['GET'])
def get_sensor_data():
    data = []
    try:
        connection = mysql.connector.connect(**config)
        connection.database = 'Arduino' # Select database
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM SensorData ORDER BY id DESC LIMIT 10")
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
    app.run(host='192.168.2.4', port=8080)
