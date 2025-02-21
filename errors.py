from http import HTTPStatus

from response import send_response


class TaskNotFoundError(Exception):
    pass

class QueryNotFoundError(Exception):
    pass

class InvalidTaskIDError(Exception):
    pass

def handle_error(handler, error):

    if isinstance(error, (TaskNotFoundError, InvalidTaskIDError, QueryNotFoundError)):
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