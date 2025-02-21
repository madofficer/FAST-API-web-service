import json
from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
from json import JSONDecodeError

from errors import TaskNotFoundError, handle_error, QueryNotFoundError, InvalidTaskDataError
from repository.task_repository import TaskRepositoryIml
from response import make_response, send_response
from usecase.task_usecases import CreateTaskUseCase, GetTaskStatusUseCase, GetTaskResultUseCase
from usecase.worker import start_task


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.task_repository = TaskRepositoryIml()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        try:
            content_len = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_len).decode("utf-8")

            try:
                task_data = json.loads(post_data)
                description = task_data.get("description")

                if not description:
                    raise InvalidTaskDataError("Description for task required")

            except json.JSONDecodeError:
                raise InvalidTaskDataError("Invalid json data")

            use_case = CreateTaskUseCase(self.task_repository)
            task = use_case.execute(description)

            response_data = make_response({
                "task_id": task.id,
                "message": "Task created"
            })

            send_response(self, HTTPStatus.CREATED, response_data)

        except JSONDecodeError:
            handle_error(self, ValueError("Invalid JSON data"))
        except Exception as err:
            handle_error(self, err)

    # query sample: curl -X GET -d "action=status&task_id=777" http://localhost:8080/
    def do_GET(self):
        try:
            http_query = self.path.split('/')
            task_id = http_query[-1]
            query_type = http_query[-2]

            use_case = GetTaskStatusUseCase(self.task_repository)
            task = use_case.execute(task_id)

            if not task:
                raise TaskNotFoundError(f"No Task:[{task_id}] Found")

            if query_type == "status":
                use_case = GetTaskStatusUseCase(self.task_repository)
                task = use_case.execute(task_id)
                response_data = make_response({
                    "task_id": task_id,
                    "task_status": task.status,
                    "task_log": task.log,
                    "task_result": task.result
                })
            elif query_type == "result":
                use_case = GetTaskResultUseCase(self.task_repository)
                task_result = use_case.execute(task_id)
                response_data = make_response({
                    "task_result": task_result
                })
            else:
                raise QueryNotFoundError(f"No Query:[{query_type}] Found")

            if response_data:
                send_response(self, HTTPStatus.OK, response_data)

        except Exception as err:
            handle_error(self, err)
