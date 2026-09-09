from http.server import BaseHTTPRequestHandler, HTTPServer

class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            message = b"Hello from Zeek's container!"
            status = 200
        elif self.path == "/health":
            message = b"OK"
            status = 200
        else:
            message = b"Not found"
            status = 404

        self.send_response(status)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(message)
server = HTTPServer(("0.0.0.0", 8000), AppHandler)
print("Server listening on port 8000", flush=True)
server.serve_forever()
