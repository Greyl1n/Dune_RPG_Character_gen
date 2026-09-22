"""Simple local launcher for the Dune Character Generator HTML Web App."""

import webbrowser
import http.server
import socketserver
import threading
from pathlib import Path

PORT = 8000


def main():
    html_file = Path(__file__).parent / "index.html"
    if not html_file.exists():
        print("Error: index.html not found!")
        return

    # Serve files from current directory
    handler = http.server.SimpleHTTPRequestHandler
    
    # Allow port reuse
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        url = f"http://localhost:{PORT}/index.html"
        print("=" * 65)
        print("⚔️  DUNE: ADVENTURES IN THE IMPERIUM — CHARACTER GENERATOR  ⚔️")
        print("=" * 65)
        print(f"Local HTML Web App is running at: {url}")
        print("Opening browser automatically...")
        print("Press Ctrl+C to stop the server.")
        print("=" * 65)
        
        # Open in default web browser
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")


if __name__ == "__main__":
    main()
