from flask import Flask, request, jsonify
from flask import Flask, render_template
import requests

communication_server = Flask(__name__)

@communication_server.route('/')
def home():
    return render_template('index.html')

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

@communication_server.route('/retrieve-sensor-data', methods=['GET'])
def retrieve_sensor_data():
    device_id = request.args.get('device_id')
    retrieve_url = f"http://127.0.0.1:5000/from-coap-server?device_id={device_id}"

    try:
        retrieve_response = requests.get(retrieve_url)
        if retrieve_response.status_code == 200:
            data = retrieve_response.content.decode()
            return jsonify({"message": "Sensor data retrieved successfully", "data": data})
        else:
            return jsonify({"message": "Failed to retrieve sensor data", "status_code": retrieve_response.status_code}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@communication_server.route('/retrieve-all-sensor-data', methods=['GET'])
def retrieve_all_sensor_data():
    retrieve_url = "http://127.0.0.1:5000/from-coap-server/all"

    try:
        retrieve_response = requests.get(retrieve_url)
        if retrieve_response.status_code == 200:
            data = retrieve_response.content.decode()
            return jsonify({"message": "All sensor data retrieved successfully", "data": data})
        else:
            return jsonify({"message": "Failed to retrieve all sensor data", "status_code": retrieve_response.status_code}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

def run_communication_server():
    communication_server.run(host='127.0.0.1', port=9999, debug=True)