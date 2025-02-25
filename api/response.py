from dataclasses import dataclass, field
import json
from http import HTTPStatus
from typing import Optional


@dataclass
class Response:
    data: dict[str, str] = field(default_factory=dict)
    message: Optional[str] = None

    def get_response(self) -> dict:
        return {"data": self.data, "message": self.message}


def send_response(handler, status_code, response_data):
    def send_headers():
        handler.send_response(status_code)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()

    def send_data(data):
        if isinstance(data, dict):
            data = json.dumps(data, indent=4)
        handler.wfile.write(data.encode() if isinstance(data, str) else data)

    if isinstance(response_data, str) and response_data.endswith(".json"):
        try:
            with open(response_data, "rb") as file:
                response_data = file.read()
                send_headers()
                send_data(response_data)
        except Exception as e:
            handler.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
            send_headers()
            send_data({"error": f"Failed to read file: {str(e)}"})
    else:
        send_headers()
        send_data(response_data)
