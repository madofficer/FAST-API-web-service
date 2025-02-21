from http.server import HTTPServer
from repository.ram_storage import RamStorage


class Server(HTTPServer):
    def __init__(self, server_addr, request_handler):
        self.db = RamStorage()
        super().__init__(server_addr, request_handler)
