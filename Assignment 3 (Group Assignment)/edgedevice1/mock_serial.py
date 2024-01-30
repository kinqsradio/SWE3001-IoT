import random
import time
import datetime

class MockSerial:
    def __init__(self, port, baudrate, timeout):
        self.in_waiting = True  # Simulate data always available

    def readline(self):
        # Generate fake sensor data
        dht_temp = round(random.uniform(20, 30), 2)  # DHT Temperature
        humidity = round(random.uniform(30, 60), 2)  # Humidity
        lm35_temp = round(random.uniform(15, 25), 2)  # LM35 Temperature
        return f"{dht_temp},{humidity},{lm35_temp}\n".encode()

    def flush(self):
        pass  # No action needed for flush in mock
