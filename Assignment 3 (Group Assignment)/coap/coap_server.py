from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon import defines
from db import create_database, create_table, retrieve_sensor_data
import json
from mysql.connector import connect, Error
from dbconfig import config

class SensorDataResource(Resource):
    def __init__(self, name="SensorDataResource"):
        super(SensorDataResource, self).__init__(name)
        self.payload = "Sensor Data Resource"

    def render_POST(self, request):
        try:
            received_data = request.payload.decode() if isinstance(request.payload, bytes) else request.payload
            print(f"Received data: {received_data}")
            sensor_data = json.loads(received_data)
            device_id = sensor_data["DeviceID"]
            self.handle_sensor_data(device_id, sensor_data)

            response = self.init_resource(request, self)
            response.payload = "Data received successfully.".encode('utf-8')
            response.code = defines.Codes.CONTENT.number
            return response
        except Exception as e:
            print(f"Error processing POST request: {e}")
            response = self.init_resource(request, self)
            response.code = defines.Codes.INTERNAL_SERVER_ERROR.number
            response.payload = "Error in data processing.".encode('utf-8')
            return response

    def handle_sensor_data(self, device_id, sensor_data):
        db_name = "SensorDataDB"
        try:
            connection = connect(**config)
            cursor = connection.cursor()
            create_database(cursor, db_name)
            connection.database = db_name
            create_table(cursor, device_id, sensor_data)

            # Preparing insert statement
            columns = ", ".join(["DeviceID", "Time"] + list(sensor_data["Data"].keys()))
            placeholders = ", ".join(["%s"] * (len(sensor_data["Data"]) + 2))
            insert_query = f"INSERT INTO {device_id}_Table ({columns}) VALUES ({placeholders})"
            data_values = [device_id, sensor_data["Timestamp"]] + list(sensor_data["Data"].values())

            cursor.execute(insert_query, data_values)
            connection.commit()
            print(f"Data inserted into {device_id}_Table")

        except Error as e:
            print(f"Database error: {e}")
        finally:
            cursor.close()
            connection.close()

class RetrieveSensorDataResource(Resource):
    def __init__(self, name="RetrieveSensorDataResource"):
        super(RetrieveSensorDataResource, self).__init__(name)
        self.payload = "Retrieve Sensor Data Resource"

    def render_GET(self, request):
        response = self.init_resource(request, self)
        try:
            connection = connect(**config, database='SensorDataDB')
            cursor = connection.cursor()
            device_id = request.uri_query.split('=')[1]

            data = retrieve_sensor_data(cursor, device_id)
            response.payload = json.dumps(data) #.encode('utf-8')  # Wrap data in a dictionary
            # response.payload = json.dumps(data) #.encode('utf-8') ## May be no need to convert to string? still works fine
            response.code = defines.Codes.CONTENT.number
            # if data:
            #     response.payload = json.dumps(data) #.encode('utf-8') ## May be no need to convert to string? still works fine
            #     response.code = defines.Codes.CONTENT.number
            # else:
            #     # Send a JSON-formatted message even when no data is found
            #     response.payload = json.dumps({"message": "No data found for the specified device ID"}) #.encode('utf-8') ## May be no need to convert to string? still works fine
            #     response.code = defines.Codes.NOT_FOUND.number
        except Error as e:
            print(f"Error retrieving data: {e}")
            response.payload = json.dumps(data)
            # response.payload = json.dumps({"error": "Error in data retrieval"}) #.encode('utf-8') ## May be no need to convert to string? still works fine
            response.code = defines.Codes.INTERNAL_SERVER_ERROR.number
        finally:
            cursor.close()
            connection.close()
        return response
    
class MyCoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource('sensor-data/', SensorDataResource())
        self.add_resource('retrieve-sensor-data/', RetrieveSensorDataResource())


def run_coap_server():
    coap_server = MyCoAPServer("127.0.0.1", 5684)
    try:
        print("CoAP Server Started")
        coap_server.listen()
    except KeyboardInterrupt:
        print("Server Shutdown")
        coap_server.close()
        print("Exiting...")

if __name__ == "__main__":
    run_coap_server()