from dataclasses import dataclass, field
import json
from typing import Optional


@dataclass
class Response:
    data: dict[str, str] = field(default_factory=dict)
    message: Optional[str] = None

    def get_response(self) -> dict:
        return {"data" : self.data, "message": self.message}


def send_response(handler, status_code, response_data):
    handler.send_response(status_code)
    handler.send_header("Content-type", "application/json")
    handler.end_headers()
    handler.wfile.write(json.dumps(response_data, indent=4).encode())

# if __name__ == "__main__":
#     x = Response(
#         {
#             "task_result": 'task_result'
#         }
#     ).to_json()
#     print(type(Response({"task_result": 'task_result'}).to_json()))
