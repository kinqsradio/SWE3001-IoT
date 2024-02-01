import random
import time

class MockSerial:
    def __init__(self, port, baudrate, timeout):
        self.in_waiting = True  # Simulate data always available

    def readline(self):
        # Simulate waiting for 2 seconds between readings
        time.sleep(2)

        # Generate fake random motion sensor data (ON or OFF)
        motion_state = random.choice(["ON", "OFF"])
        return f"{motion_state}\n".encode()

    def flush(self):
        pass  # No action needed for flush in mock