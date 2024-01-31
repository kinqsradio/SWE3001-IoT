from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/communication-sensor-data', methods=['POST'])
def receive_sensor_data():
    data = request.json
    print("Received data from Edge Device:", data)

    # Forward this data to another server, you can do so here.
    # For example, forwarding to 127.0.0.1:9999
    forward_url = "http://127.0.0.1:5000/coap-server"
    try:
        forward_response = requests.post(forward_url, json=data)
        if forward_response.status_code == 200:
            return jsonify({"message": "Data forwarded successfully to COAP Server", "forward_response": forward_response.text})
        else:
            return jsonify({"message": "Failed to forward data", "status_code": forward_response.status_code}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9999, debug=True)
