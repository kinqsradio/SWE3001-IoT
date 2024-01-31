from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon import defines

# CoAP Server Setup
class SensorDataResource(Resource):
    def __init__(self, name="SensorDataResource"):
        super(SensorDataResource, self).__init__(name)
        self.payload = "Sensor Data Resource"

    def render_POST(self, request):
        try:
            received_data = request.payload.decode() if isinstance(request.payload, bytes) else request.payload
            print(f"Received data: {received_data}")
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