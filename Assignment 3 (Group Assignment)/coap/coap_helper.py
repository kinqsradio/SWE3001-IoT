import json
from coapthon.client.helperclient import HelperClient

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