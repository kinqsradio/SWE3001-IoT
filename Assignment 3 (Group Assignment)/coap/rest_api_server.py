import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from coap_helper import forward_to_coap_server
from db import get_all_device_ids

# Flask App Setup
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route('/to-coap-server', methods=['POST'])
def receive_and_forward_data():
    data = request.json
    print("Received data from COMMUNICATION client:", data)
    coap_response = forward_to_coap_server(data)
    return jsonify({"message": "Data forwarded to CoAP server", "coap_response": coap_response})



def run_flask_app():
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)