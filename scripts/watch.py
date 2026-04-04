import socket
import subprocess

from livereload import Server

from .build import BUILD_DIR, ROOT


def get_local_ip() -> str:
    try:
        # Create a socket and connect to an external server to determine the local IP
        # We don't actually send any data.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def build() -> None:
    print("Changes detected, running build...")
    subprocess.run(["python", "-m", "scripts.build"])


if __name__ == "__main__":
    # Run the initial build
    build()

    server = Server()
    # Watch directories for changes
    server.watch(str(ROOT / "notebooks" / "*.ipynb"), build)
    server.watch(str(ROOT / "template"), build)
    server.watch(str(ROOT / "scripts"), build)
    server.watch(str(ROOT / "registry.json"), build)
    server.watch(str(ROOT / "authors.json"), build)

    # Serve the build directory
    local_ip = get_local_ip()
    print("Starting live-reload server...")
    print("Local:   http://localhost:8000")
    print(f"Network: http://{local_ip}:8000")
    server.serve(root=str(BUILD_DIR), port=8000, host="0.0.0.0")
