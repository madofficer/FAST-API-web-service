from http import HTTPStatus


class TaskNotFoundError(Exception):
    pass

class InvalidTaskIDError(Exception):
    pass

def handle_error(handler, error):

    if isinstance(error, (TaskNotFoundError, InvalidTaskIDError)):
        status_code = HTTPStatus.NOT_FOUND
        response_data = {
            "status": "error",
            "message": str(error)
        }

    else:
        status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        response = {
            "status": "error",
            "message": "An unexpected error occurred"
        }