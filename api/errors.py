from http import HTTPStatus
from api.response import send_response


class BaseTaskError(Exception):
    @staticmethod
    def get_status():
        pass


class BaseTaskNotFoundError(BaseTaskError):
    @staticmethod
    def get_status() -> HTTPStatus:
        return HTTPStatus.NOT_FOUND


class BaseInvalidDataError(BaseTaskError):
    @staticmethod
    def get_status() -> HTTPStatus:
        return HTTPStatus.BAD_REQUEST


class TaskNotFoundError(BaseTaskNotFoundError):
    pass


class QueryNotFoundError(BaseTaskNotFoundError):
    pass


class InvalidTaskDataError(BaseInvalidDataError):
    pass


class InvalidTaskIDError(BaseInvalidDataError):
    pass


def handle_error(handler, error):
    if isinstance(error, BaseTaskError):
        status_code = error.get_status()
        message = str(error)
        if not message:
            message = repr(error)
        response_data = {"message": message}

    else:
        status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        response_data = {"message": "An unexpected error occurred"}

    send_response(handler, status_code, response_data)
