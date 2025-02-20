import json


def make_response(data):
    return {
        "status": "success",
        "data": data
    }


def send_response(handler, status_code, response_data):
    handler.send_response(status_code)
    handler.send_header("Content-type", "application/json")
    handler.send_headers()
    handler.wfile.write(json.dumps(response_data, indent=4).encode())
