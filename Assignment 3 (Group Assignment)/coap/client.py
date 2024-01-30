from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon import defines

class SensorDataResource(Resource):
    def __init__(self, name="SensorDataResource"):
        super(SensorDataResource, self).__init__(name)
        self.payload = "Sensor Data Resource"

    def render_POST(self, request):
        try:
            # Check if payload is bytes and decode if necessary
            if isinstance(request.payload, bytes):
                received_data = request.payload.decode()
            else:
                received_data = request.payload  # Payload is already a string

            print(f"Received data: {received_data}")

            # Prepare response
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


class MyCoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource('sensor-data/', SensorDataResource())

def main():
    server = MyCoAPServer("127.0.0.1", 5683)
    try:
        print("CoAP Server Started")
        server.listen()
    except KeyboardInterrupt:
        print("Server Shutdown")
        server.close()
        print("Exiting...")

if __name__ == "__main__":
    main()
