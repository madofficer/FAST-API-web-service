from http import HTTPStatus

from api.response import send_response

class BaseTaskError(Exception):
    pass

class TaskNotFoundError(BaseTaskError):
    pass

class QueryNotFoundError(BaseTaskError):
    pass

class InvalidTaskDataError(BaseTaskError):
    pass

class InvalidTaskIDError(BaseTaskError):
    pass

def handle_error(handler, error):

    if isinstance(error, BaseTaskError):
        status_code = HTTPStatus.NOT_FOUND
        response_data = {
            "status": "error",
            "message": str(error)
        }

    else:
        status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        response_data = {
            "status": "error",
            "message": "An unexpected error occurred"
        }

    send_response(handler, status_code, response_data)