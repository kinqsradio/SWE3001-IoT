import datetime
import serial
import time
from mock_serial import MockSerial

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
                        "DHTTemperature": dht_temp,
                        "Humidity": humidity,
                        "LM35Temperature": lm35_temp,
                        "Time": current_datetime
                    }
                    yield sensor_data
                except ValueError as e:
                    print(f"Error parsing data: {e}")
            else:
                print("Incomplete data received")
        time.sleep(1)  # Small delay to prevent CPU overuse
