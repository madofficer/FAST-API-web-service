import json
from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
from json import JSONDecodeError

from errors import TaskNotFoundError, handle_error, QueryNotFoundError
from response import make_response, send_response
from worker import start_task


class RequestHandler(BaseHTTPRequestHandler):
    @property
    def db(self):
        return self.server.db

    # query sample: curl -X GET -d "action=status&task_id=777" http://localhost:8080/
    def do_GET(self):
        print('GET')

        try:
            http_query = self.path.split('/')
            task_id = http_query[-1]
            query_type = http_query[-2]

            task = self.db.get_task(task_id)
            if not task:
                raise TaskNotFoundError(f"No Task:[{task_id}] Found")

            if query_type == "status":
                response_data = make_response({
                    "task_id": task_id,
                    "task_status": task["status"],
                    "task_log": task["log"],
                    "task_result": task["result"]
                })
            elif query_type == "result":
                response_data = make_response({
                    "task_result": task["result"]
                })
            else:
                raise QueryNotFoundError(f"No Query:[{query_type}] Found")

            if response_data:
                send_response(self, HTTPStatus.OK, response_data)

        except Exception as err:
            handle_error(self, err)

    def do_POST(self):
        print('POST')
        try:
            content_len = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_len).decode("utf-8")

            task_data = json.loads(post_data)
            task_id = self.db.create_task(task_data)

            response_data = make_response({
                "task_id": task_id,
                "status": "Task created successfully"
            })
            send_response(self, HTTPStatus.CREATED, response_data)
            start_task(self.db, task_id)

        except JSONDecodeError:
            handle_error(self, ValueError("Invalid JSON data"))
        except Exception as err:
            handle_error(self, err)
