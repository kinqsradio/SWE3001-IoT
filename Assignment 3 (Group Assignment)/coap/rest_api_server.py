import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from coap_helper import forward_to_coap_server
from config import config
from db_helper import get_all_device_ids
from mysql.connector import connect, Error

# Flask App Setup
app = Flask(__name__)
CORS(app)

"""
Send Sensor Data to CoAP Server
"""
@app.route('/to-coap-server', methods=['POST'])
def receive_and_forward_data():
    data = request.json
    print("Received data from COMMUNICATION client:", data)
    coap_response = forward_to_coap_server(data)
    return jsonify({"message": "Data forwarded to CoAP server", "coap_response": coap_response})

@app.route('/retrieve-sensor-data', methods=['GET'])
def retrieve_sensor_data():
    try:
        connection = connect(**config)
        cursor = connection.cursor()
        connection.database = "SensorDataDB"
        device_ids = get_all_device_ids(cursor)
        print(f"Device IDs: {device_ids}")
    except:
        device_ids = []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return jsonify({"device_ids": device_ids})




def run_flask_app():
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)
    
    
device_ids = retrieve_sensor_data()