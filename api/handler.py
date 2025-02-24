import json
from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
from json import JSONDecodeError

from api.errors import (
    TaskNotFoundError,
    handle_error,
    QueryNotFoundError,
    InvalidTaskDataError,
)
from api.response import make_response, send_response
from usecase.task_usecases import (
    CreateTaskUseCase,
    GetTaskStatusUseCase,
    GetTaskResultUseCase,
)


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, task_repository, *args, **kwargs):
        self.task_repository = task_repository
        super().__init__(*args, **kwargs)

    def do_POST(self):
        try:
            content_len = int(self.headers.get("Content-Length", 0))
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

            response_data = make_response(
                {"task_id": task.id}
            ).to_json()

            send_response(self, HTTPStatus.CREATED, response_data)

        except JSONDecodeError:
            handle_error(self, ValueError("Invalid JSON data"))
        except Exception as err:
            handle_error(self, err)

    def do_GET(self):
        try:
            http_query = self.path.split("/")
            task_id = http_query[-1]
            query_type = http_query[-2]

            use_case = GetTaskStatusUseCase(self.task_repository)
            task = use_case.execute(task_id)

            if not task:
                raise TaskNotFoundError(f"No Task:[{task_id}] Found")

            if query_type == "status":
                response_data = self._get_task_status(task_id)
            elif query_type == "result":
                response_data = self._get_task_result(task_id)
            else:
                raise QueryNotFoundError(f"No Query:[{query_type}] Found")

            if response_data:
                send_response(self, HTTPStatus.OK, response_data)

        except Exception as err:
            handle_error(self, err)

    def _get_task_status(self, task_id) -> json:
        use_case = GetTaskStatusUseCase(self.task_repository)
        task = use_case.execute(task_id)
        response_data = make_response(
            {
                "task_status": task.status,
                "task_log": task.log,
                "task_result": task.result,
            }
        ).to_json()
        return response_data

    def _get_task_result(self, task_id):
        use_case = GetTaskResultUseCase(self.task_repository)
        task_result = use_case.execute(task_id)
        response_data = make_response({"task_result": task_result}).to_json()
        return response_data
