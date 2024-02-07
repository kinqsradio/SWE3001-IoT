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
            parts = line.split(',')
            if len(parts) == 3:
                try:
                    dht_temp = float(parts[0])
                    humidity = float(parts[1])
                    lm35_temp = float(parts[2])
                    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    sensor_data = {
                        "DeviceID": "TemperatureHumidity_01",
                        "DeviceType": "TemperatureHumidity",
                        "Timestamp": current_datetime,
                        "Data": {
                            "DHTTemperature": dht_temp,
                            "Humidity": humidity,
                            "LM35Temperature": lm35_temp
                        }
                    }
                    yield sensor_data
                except ValueError as e:
                    print(f"Error parsing data: {e}")
            else:
                print("Incomplete data received")
        time.sleep(1)  # Small delay to prevent CPU overuse

# CoAP Server connection details
COAP_SERVER_HOST = "127.0.0.1"
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
