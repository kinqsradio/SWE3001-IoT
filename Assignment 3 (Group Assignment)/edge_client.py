import requests
import time
from get_data import get_sensor_data  # Importing the get_sensor_data function

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

def main():
    comm_server_url = "http://cb4ckwgp-9999.auc1.devtunnels.ms/communication-sensor-data"

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
