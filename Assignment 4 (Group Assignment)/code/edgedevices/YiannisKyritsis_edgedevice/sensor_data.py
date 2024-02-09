import datetime
import serial
import time
from mock_serial import MockSerial
import requests
import json
from coapthon.client.helperclient import HelperClient

def get_sensor_data(use_mock=False):
    ser = MockSerial('/dev/ttyUSB0', 9600, timeout=1) if use_mock else serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.flush()

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            if line in ["Motion detected", "Motion not detected"]:
                try:
                    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    motion_status = "Motion detected" if line == "Motion detected" else "Motion not detected"
                    sensor_data = {
                        "DeviceID": "MotionSensor_01",
                        "DeviceType": "MotionSensor",
                        "Timestamp": current_datetime,
                        "Data": {
                            "MotionStatus": motion_status
                        }
                    }
                    yield sensor_data
                except ValueError as e:
                    print(f"Error parsing data: {e}")
            else:
                print("Invalid data received")
        time.sleep(2)
        
        
# CoAP Server connection details
COAP_SERVER_HOST = ""
COAP_SERVER_PORT = 5684
SENSOR_DATA_RESOURCE_PATH = "sensor-data"

def send_data_to_coap_server(data):
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

def send_data_to_comm_server(data, url):
    """Send data to the Communication Server."""
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f"Data sent successfully. Server responded: {response.text}")
        else:
            print(f"Failed to send data. Server responded with status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")