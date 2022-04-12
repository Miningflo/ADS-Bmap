import http
from http.server import BaseHTTPRequestHandler


class MyHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, planelist):
        self.planelist = planelist

    def __call__(self, *args, **kwargs):
        """Handle a request."""
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        try:
            self.wfile.write(self.planelist.json().encode("utf-8"))
        except ConnectionError:
            print("Continue")

    def log_message(self, format, *args):
        return




