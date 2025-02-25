from http.server import HTTPServer

from api.config.config_interface import parse_config
from api.handler import RequestHandler
from repository.task_repository import TaskRepositoryIml


class Server(HTTPServer):
    def __init__(self, server_addr, request_handler):
        self.task_repository = TaskRepositoryIml()

        def handler(*args, **kwargs):
            return request_handler(self.task_repository, *args, **kwargs)

        super().__init__(server_addr, handler)


def run_server(server_address=None):
    if server_address is None:
        server_address = parse_config().get_address()
    http_server = Server(server_address, RequestHandler)
    print(f"Server started on {server_address[0]}:{server_address[1]}")
    http_server.serve_forever()
