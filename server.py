import http.server


class MyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, planelist):
        self.planelist = planelist

    def __call__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def log_message(self, format, *args):
        return

    def do_GET(self):
        try:
            if self.path != '/api':
                self.path = "./frontend" + self.path
                return http.server.SimpleHTTPRequestHandler.do_GET(self)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(self.planelist.json().encode("utf-8"))
        except Exception as e:
            print(e)

        return
