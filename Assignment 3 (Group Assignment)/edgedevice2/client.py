import requests
import time
from sensor_data import get_sensor_data, send_data_to_comm_server  # Importing the get_sensor_data function

def main():
    # comm_server_url = "http://127.0.0.1:9999/forward-edge-data"
    comm_server_url = "https://r3n83zqx-9999.aue.devtunnels.ms/forward-edge-data"
    
    # Create a generator instance
    sensor_data_generator = get_sensor_data(use_mock=True)  # Set use_mock=False for real data

    while True:
        try:
            data = next(sensor_data_generator)  # Fetch next item from generator
            print("Data to send:", data)
            send_data_to_comm_server(data, comm_server_url)
            time.sleep(1)  # Adjust time as necessary
        except StopIteration:
            print("No more data from the sensor.")
            break
        except Exception as e:
            print(f"Error while getting sensor data: {e}")
            break

if __name__ == "__main__":
    main()
