import random
import time

class MockSerial:
    def __init__(self, port, baudrate, timeout):
        self.in_waiting = True  # Simulate data always available

    def readline(self):
        # Simulate waiting for 2 seconds between readings
        time.sleep(2)

        # Generate random motion sensor data (ON or OFF)
        motion_state = random.choice(["ON", "OFF"])
        return f"{motion_state}\n".encode()

    def flush(self):
        pass  # No action needed for flush in mock

# Test routine to print mock data
if __name__ == "__main__":
    mock = MockSerial('COM1', 9600, 1)  # Example port, baudrate, and timeout
    for _ in range(10):  # Read and print 10 lines of data
        data = mock.readline().decode()  # Decoding the encoded string
        print(data.strip())  # Print data
