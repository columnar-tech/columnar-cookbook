from livereload import Server
from .build import ROOT, BUILD_DIR
import subprocess

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
    print(f"Starting live-reload server on http://localhost:8000")
    server.serve(root=str(BUILD_DIR), port=8000)
