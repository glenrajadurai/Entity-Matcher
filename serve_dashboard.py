import http.server
import socketserver
import webbrowser
import os

PORT = 8000
DIRECTORY = "web"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def serve_dashboard():
    os.makedirs(DIRECTORY, exist_ok=True)
    with ReusableTCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"Serving ER Dashboard website at: {url}")
        webbrowser.open(url)
        httpd.serve_forever()


if __name__ == "__main__":
    serve_dashboard()
