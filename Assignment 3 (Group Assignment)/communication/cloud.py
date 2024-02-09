from flask import Flask, request, jsonify
from flask import Flask, render_template
import requests
import json
from flask_cors import CORS
from config import config
from db_helper import get_all_device_ids, retrieve_data
from mysql.connector import connect, Error

communication_server = Flask(__name__)
CORS(communication_server)

"""
This is a quick backup method for group member to easily port data to the CoAP server.
As Visual Studio Code does not support CoAP protocol, this will be a quick way to send data to the CoAP server.
CoAP Protocol has been successfully tested by Anh and it works perfectly!
THIS OPTION WILL BE DISBLED ON THE EDGE DEVICES THAT RECEIVED DATA FROM ADRUINO ON TEAM MEMBERS FOR COAP PROTOCOL!
"""
@communication_server.route('/forward-edge-data', methods=['POST'])
def forward_edge_data():
    data = request.json
    # print("Received data from Edge Device:", data)
    print(f"Received data from {data['DeviceType']} (ID: {data['DeviceID']}) at {data['Timestamp']}: {data['Data']}")

    forward_url = "http://127.0.0.1:5000/to-coap-server"
    try:
        forward_response = requests.post(forward_url, json=data)
        if forward_response.status_code == 200:
            # Send a simple acknowledgment to the edge device
            return jsonify({"message": "Data received and forwarded successfully"})
        else:
            return jsonify({"message": "Failed to forward data", "status_code": forward_response.status_code}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


"""
Retrieve all sensor data from the database and return it as a JSON object.
THIS IS THE API THAT WILL BE USING TO DISPLAY TO USER INTERFACE
"""
@communication_server.route('/retrieve-all-sensor-data', methods=['GET'])
def retrieve_all_sensor_data():
    aggregated_data = []  
    try:
        connection = connect(**config)  
        cursor = connection.cursor()
        connection.database = "SensorDataDB"  
        device_ids = get_all_device_ids(cursor)  
        
        for device_id in device_ids:
            device_data = retrieve_data(cursor, device_id) 
            # Append device data to the aggregated list
            aggregated_data.append({"device_id": device_id, "data": device_data})
    except Error as e:
        print(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500  
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close() 

    return jsonify(aggregated_data)

@communication_server.route('/')
def home():
    try:
        data = retrieve_all_sensor_data().get_json()
        return render_template('index.html', data=data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



def run_communication_server():
    communication_server.run(host='127.0.0.1', port=9999, debug=True)