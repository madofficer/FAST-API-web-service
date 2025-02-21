from http.server import HTTPServer

from api.handler import RequestHandler
from repository.task_repository import TaskRepositoryIml


class Server(HTTPServer):
    def __init__(self, server_addr, request_handler):
        self.task_repository = TaskRepositoryIml()
        def handler(*args, **kwargs):
            return request_handler(
                self.task_repository,
                *args,
                **kwargs
            )
        super().__init__(server_addr, handler)

def run_server(host, port):
    server_address = (host, port)
    http_server = Server(server_address, RequestHandler)
    print(f"Server started on {host}:{port}")
    http_server.serve_forever()