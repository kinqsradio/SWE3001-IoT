from coapthon.client.helperclient import HelperClient
from get_data import get_sensor_data  # Importing the get_sensor_data function
import json
import time

def send_to_coap_server(host, port, path, data):
    """Send data to the CoAP server."""
    client = HelperClient(server=(host, port))
    try:
        response = client.post(path, json.dumps(data))
        if response:
            # Ensure that response payload is not None
            payload = response.payload.decode() if response.payload else "No payload"
            print(f"Result: {response.code} - {payload}")
        else:
            print("No response received from the server.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.stop()

def main():
    host = "127.0.0.1"  # CoAP server address
    port = 5683         # CoAP server port
    path = "sensor-data" # CoAP resource path

    # Create a generator instance
    sensor_data_generator = get_sensor_data(use_mock=True)

    while True:
        try:
            data = next(sensor_data_generator)  # Fetch next item from generator
            print("Data to send:", data)
            send_to_coap_server(host, port, path, data)
            time.sleep(1)  # Adjust time as necessary
        except StopIteration:
            print("No more data from the sensor.")
            break
        except Exception as e:
            print(f"Error while getting sensor data: {e}")
            break

if __name__ == "__main__":
    main()
