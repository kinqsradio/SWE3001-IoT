import threading
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from coapthon.client.helperclient import HelperClient

# Flask App Setup
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# CoAP Server connection details
COAP_SERVER_HOST = "127.0.0.1"
COAP_SERVER_PORT = 5684
COAP_RESOURCE_PATH = "sensor-data"

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

@app.route('/to-coap-server', methods=['POST'])
def receive_and_forward_data():
    data = request.json
    print("Received data from COMMUNICATION client:", data)
    coap_response = forward_to_coap_server(data)
    return jsonify({"message": "Data forwarded to CoAP server", "coap_response": coap_response})

def run_flask_app():
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)

if __name__ == "__main__":
    run_flask_app()

