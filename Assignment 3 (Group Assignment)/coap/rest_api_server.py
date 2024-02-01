import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from coapthon.client.helperclient import HelperClient
from db import get_all_device_ids
# Flask App Setup
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# CoAP Server connection details
COAP_SERVER_HOST = "127.0.0.1"
COAP_SERVER_PORT = 5684
COAP_RESOURCE_PATH = "sensor-data"
COAP_RETRIEVE_RESOURCE_PATH = "retrieve-sensor-data"

def forward_to_coap_server(data):
    client = HelperClient(server=(COAP_SERVER_HOST, COAP_SERVER_PORT))
    try:
        response = client.post(COAP_RESOURCE_PATH, json.dumps(data))
        if response and response.payload:
            return f"CoAP Response: {response.payload.decode()}"
        else:
            return "No response or empty payload from CoAP server"
    except Exception as e:
        return f"An error occurred while sending to CoAP server: {e}"
    finally:
        client.stop()

### Here is a problem
def retrieve_from_coap_server(device_id):
    client = HelperClient(server=(COAP_SERVER_HOST, COAP_SERVER_PORT))
    try:
        response = client.get(f"{COAP_RETRIEVE_RESOURCE_PATH}?device_id={device_id}")
        if response and response.payload:
            # Convert the payload to JSON
            return json.loads(response.payload.decode())
        else:
            return None
    except Exception as e:
        return f"An error occurred while retrieving from CoAP server: {e}"
    finally:
        client.stop()

@app.route('/to-coap-server', methods=['POST'])
def receive_and_forward_data():
    data = request.json
    print("Received data from COMMUNICATION client:", data)
    coap_response = forward_to_coap_server(data)
    return jsonify({"message": "Data forwarded to CoAP server", "coap_response": coap_response})

@app.route('/from-coap-server', methods=['GET'])
def get_sensor_data():
    device_id = request.args.get('device_id')
    if not device_id:
        return jsonify({"error": "Device ID is required"}), 400

    coap_response = retrieve_from_coap_server(device_id)
    if coap_response is not None:
        return jsonify({"message": "Data retrieved from CoAP server", "data": coap_response})
    else:
        return jsonify({"error": "Failed to retrieve data or empty response from CoAP server"}), 500


@app.route('/from-coap-server/all', methods=['GET'])
def get_all_sensor_data():
    all_device_ids = get_all_device_ids()
    all_data = {}

    for device_id in all_device_ids:
        response = retrieve_from_coap_server(device_id)
        if response is not None:
            all_data[device_id] = response

    return jsonify({"message": "Data retrieved from CoAP server for all devices", "data": all_data})

def run_flask_app():
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)