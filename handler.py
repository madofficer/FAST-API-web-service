from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
from urllib.parse import urlparse, parse_qs


class RequestHandler(BaseHTTPRequestHandler):
    @property
    def db(self):
        return self.server.db

    # query sample: curl -X GET -d "action=status&task_id=777" http://localhost:8080/
    def do_GET(self):

        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        action = query_params.get('action', [None])[0]
        task_id = query_params.get('task_id', [None])[0]

        if action in ('status', 'result'):
            self.send_response(HTTPStatus.OK)


        else:
            self.send_response(HTTPStatus.BAD_REQUEST)


