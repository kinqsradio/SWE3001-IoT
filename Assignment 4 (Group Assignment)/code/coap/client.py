import threading
from coap_server import run_coap_server
from rest_api_server import run_flask_app

if __name__ == "__main__":
    # Create threads for CoAP server and Flask REST API server
    coap_thread = threading.Thread(target=run_coap_server)
    flask_thread = threading.Thread(target=run_flask_app)

    # Start the servers
    coap_thread.start()
    flask_thread.start()

    # Wait for both servers to complete their execution
    coap_thread.join()
    flask_thread.join()