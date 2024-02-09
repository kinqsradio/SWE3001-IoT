import random
import time

class MockSerial:
    def __init__(self, port, baudrate, timeout):
        self.in_waiting = True  # Simulate data always available

    def readline(self):
        # Simulate waiting for 2 seconds between readings
        time.sleep(2)

        motion_state = random.choice(["Motion detected", "Motion not detected"])
        return f"{motion_state}\n".encode()

    def flush(self):
        pass  # No action needed for flush in mock