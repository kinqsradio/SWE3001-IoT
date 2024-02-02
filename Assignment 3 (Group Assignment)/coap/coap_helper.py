import json
from coapthon.client.helperclient import HelperClient

"""
This will be use to send data to the CoAP server!
As we are opening port as HTTP/HTTPS, we wont be able to send data to the CoAP server directly.

There were another option that can be use in edgedevices to send data directly to CoAP server through CoAP protocol.
This will be just a back up case if we are not able to send data to the CoAP server directly.
"""
# CoAP Server connection details
COAP_SERVER_HOST = "127.0.0.1"
COAP_SERVER_PORT = 5684
SENSOR_DATA_RESOURCE_PATH = "sensor-data"

def forward_to_coap_server(data):
    client = HelperClient(server=(COAP_SERVER_HOST, COAP_SERVER_PORT))
    try:
        response = client.post(SENSOR_DATA_RESOURCE_PATH, json.dumps(data))
        if response and response.payload:
            return f"CoAP Response: {response.payload.decode()}"
        else:
            return "No response or empty payload from CoAP server"
    except Exception as e:
        return f"An error occurred while sending to CoAP server: {e}"
    finally:
        client.stop()