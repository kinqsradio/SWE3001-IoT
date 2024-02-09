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
This is a quick backup method for group member to easily port data to the CoAP server.
As Visual Studio Code does not support CoAP protocol, this will be a quick way to send data to the CoAP server.
CoAP Protocol has been successfully tested by Anh and it works perfectly!
"""
@app.route('/to-coap-server', methods=['POST'])
def receive_and_forward_data():
    data = request.json
    print("Received data from COMMUNICATION client:", data)
    coap_response = forward_to_coap_server(data)
    return jsonify({"message": "Data forwarded to CoAP server", "coap_response": coap_response})



def run_flask_app():
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)