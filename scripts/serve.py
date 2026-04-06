import http.server
import socketserver

from .build import BUILD_DIR
from .watch import get_local_ip


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BUILD_DIR), **kwargs)


if __name__ == "__main__":
    PORT = 8000

    # We use ThreadingTCPServer instead of TCPServer for better performance
    # but regular TCPServer is fine here as it's just for local serving
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        local_ip = get_local_ip()
        print("Serving HTTP statically from 'build' directory...")
        print(f"Local:   http://localhost:{PORT}")
        print(f"Network: http://{local_ip}:{PORT}")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            httpd.server_close()
