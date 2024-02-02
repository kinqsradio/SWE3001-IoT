import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from coap_helper import forward_to_coap_server
from config import config
from db_helper import get_all_device_ids, retrieve_data
from mysql.connector import connect, Error

# Flask App Setup
app = Flask(__name__)
CORS(app)

"""
This will be use to send data to the CoAP server!
As we are opening port as HTTP/HTTPS, we wont be able to send data to the CoAP server directly.

There were another option that can be use in edgedevices to send data directly to CoAP server through CoAP protocol.
This will be just a back up case if we are not able to send data to the CoAP server directly.
"""
@app.route('/to-coap-server', methods=['POST'])
def receive_and_forward_data():
    data = request.json
    print("Received data from COMMUNICATION client:", data)
    coap_response = forward_to_coap_server(data)
    return jsonify({"message": "Data forwarded to CoAP server", "coap_response": coap_response})


"""
Retrieve sensor data from the database and return it in JSON format
"""
@app.route('/retrieve-sensor-data', methods=['GET'])
def retrieve_sensor_data():
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


def run_flask_app():
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)