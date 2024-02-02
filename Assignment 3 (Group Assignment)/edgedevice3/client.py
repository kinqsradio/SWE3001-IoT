import requests
import time
from sensor_data import get_sensor_data, send_data_to_comm_server, send_data_to_coap_server

def main(coap: bool = False):
    # comm_server_url = "http://127.0.0.1:9999/forward-edge-data"
    comm_server_url = "https://r3n83zqx-9999.aue.devtunnels.ms/forward-edge-data"
    
    # Create a generator instance
    sensor_data_generator = get_sensor_data(use_mock=True)  # Set use_mock=False for real data

    while True:
        try:
            data = next(sensor_data_generator)  # Fetch next item from generator
            print("Data to send:", data)
            if coap:
                send_data_to_coap_server(data)
            else:
                send_data_to_comm_server(data, comm_server_url)
            time.sleep(1)  # Adjust time as necessary
        except StopIteration:
            print("No more data from the sensor.")
            break
        except Exception as e:
            print(f"Error while getting sensor data: {e}")
            break

if __name__ == "__main__":
    main(coap=False)
