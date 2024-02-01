import datetime
import serial
import time
from mock_serial import MockSerial
import requests

def get_sensor_data(use_mock=False):
    ser = MockSerial('/dev/ttyUSB0', 9600, timeout=1) if use_mock else serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.flush()

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            if line in ["ON", "OFF"]:
                try:
                    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    motion_status = "Motion Detected" if line == "ON" else "Motion Not Detected"
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
        time.sleep(2)  # Adjust to match the sensor's frequency

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