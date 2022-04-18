import http
from http.server import BaseHTTPRequestHandler


class MyHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, planelist):
        self.planelist = planelist

    def __call__(self, *args, **kwargs):
        """Handle a request."""
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == "/api":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            try:
                self.wfile.write(self.planelist.json().encode("utf-8"))
            except ConnectionError:
                print("Continue")
        elif self.path in ["/", "/style.css", "script.js", "index.html"]:
            ctype = "text/html"
            if self.path == "/style.css":
                ctype = "text/css"
            elif self.path == "/script.js":
                ctype = "text/javascript"

            self.send_response(200)
            self.send_header("Content-type", ctype)
            self.end_headers()

            if self.path == "/":
                self.path += "index.html"
            try:
                with open("./frontend" + self.path, 'rb') as file:
                    self.wfile.write(file.read())
            except ConnectionError:
                print("Continue")
            except FileNotFoundError:
                pass

    def log_message(self, format, *args):
        return
