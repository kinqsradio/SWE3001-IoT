import random
import time

class MockSerial:
    def __init__(self, port, baudrate, timeout):
        self.in_waiting = True  # Simulate data always available

    def readline(self):
        # Simulate waiting for 2 seconds between readings
        time.sleep(2)

        water_level = random.uniform(0, 100)  # Simulate water level between 0 and 100
        return f"{water_level}\n".encode()

    def flush(self):
        pass  # No action needed for flush in mock