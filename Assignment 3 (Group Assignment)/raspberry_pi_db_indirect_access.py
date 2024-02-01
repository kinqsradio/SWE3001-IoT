from flask import Flask, request, Response, stream_with_context, redirect
import requests
from urllib.parse import urljoin

app = Flask(__name__)

RASPBERRY_PI_URL = 'http://192.168.1.177/phpmyadmin'

# Use Session object to persist cookies
session = requests.Session()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    global RASPBERRY_PI_URL
    url = urljoin(RASPBERRY_PI_URL, path)

    # Forward the headers we received, modifying or removing as necessary
    headers = {key: value for key, value in request.headers if key != 'Host'}
    
    # Make the request on behalf of the user
    if request.method == 'GET':
        resp = session.get(url, headers=headers, allow_redirects=False, stream=True)
    elif request.method == 'POST':
        resp = session.post(url, headers=headers, data=request.form, json=request.json, allow_redirects=False, stream=True)
    else:
        # Implement other methods as needed
        return 'Method not supported', 405

    # Stream the response back to the client
    response = Response(stream_with_context(resp.iter_content()), content_type=resp.headers['Content-Type'], status=resp.status_code)
    # Copy relevant headers from the response
    excluded_headers = ['Content-Length', 'Content-Encoding', 'Transfer-Encoding', 'Connection']
    for key, value in resp.headers.items():
        if key not in excluded_headers:
            response.headers[key] = value

    # Handle redirects
    if resp.status_code in (301, 302, 303, 307, 308):
        new_location = resp.headers.get('Location')
        if new_location:
            return redirect(new_location, code=resp.status_code)

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)