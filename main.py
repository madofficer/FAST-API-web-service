from handler import RequestHandler
from server import Server

HOST = 'localhost'
PORT = 8080

def run_server(host=HOST, port=PORT):
    server_addr = (host, port)
    http_server = Server(server_addr, RequestHandler)
    print(f"Server started on {host}:{port}")
    http_server.serve_forever()

if __name__ == "__main__":
    run_server()