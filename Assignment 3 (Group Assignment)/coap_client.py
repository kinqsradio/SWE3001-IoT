import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
from coapthon.client.helperclient import HelperClient
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon import defines
import json

# Flask App Setup
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# CoAP Server Setup
class SensorDataResource(Resource):
    def __init__(self, name="SensorDataResource"):
        super(SensorDataResource, self).__init__(name)
        self.payload = "Sensor Data Resource"

    def render_POST(self, request):
        try:
            received_data = request.payload.decode() if isinstance(request.payload, bytes) else request.payload
            print(f"Received data: {received_data}")
            response = self.init_resource(request, self)
            response.payload = "Data received successfully.".encode('utf-8')
            response.code = defines.Codes.CONTENT.number
            return response
        except Exception as e:
            print(f"Error processing POST request: {e}")
            response = self.init_resource(request, self)
            response.code = defines.Codes.INTERNAL_SERVER_ERROR.number
            response.payload = "Error in data processing.".encode('utf-8')
            return response

class MyCoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource('sensor-data/', SensorDataResource())

# Forwarding Function
coap_server_host = "127.0.0.1"
coap_server_port = 5684
coap_resource_path = "sensor-data"

def forward_to_coap_server(data):
    client = HelperClient(server=(coap_server_host, coap_server_port))
    try:
        response = client.post(coap_resource_path, json.dumps(data))
        if response and response.payload:
            return f"CoAP Response: {response.payload.decode()}"
        else:
            return "No response or empty payload from CoAP server"
    except Exception as e:
        return f"An error occurred while sending to CoAP server: {e}"
    finally:
        client.stop()

@app.route('/coap-server', methods=['POST'])
def receive_and_forward_data():
    data = request.json
    print("Received data from COMMUNICATION client:", data)
    coap_response = forward_to_coap_server(data)
    return jsonify({"message": "Data forwarded to CoAP server", "coap_response": coap_response})

# Running Flask App
def run_flask_app():
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)

# Running CoAP Server
def run_coap_server():
    coap_server = MyCoAPServer("0.0.0.0", 5684)
    try:
        print("CoAP Server Started")
        coap_server.listen()
    except KeyboardInterrupt:
        print("Server Shutdown")
        coap_server.close()
        print("Exiting...")

# Main Execution with Threading
if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask_app)
    coap_thread = threading.Thread(target=run_coap_server)

    flask_thread.start()
    coap_thread.start()

    flask_thread.join()
    coap_thread.join()
