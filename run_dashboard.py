#!/usr/bin/env python3

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

# Change to the project directory
os.chdir(Path(__file__).parent)

PORT = 8080

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers for local file access
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

print(f"Starting trading dashboard server on port {PORT}")
print(f"Dashboard URL: http://localhost:{PORT}/dashboard.html")
print("Press Ctrl+C to stop the server")

# Start the server
with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    # Open browser automatically
    webbrowser.open(f'http://localhost:{PORT}/dashboard.html')
    httpd.serve_forever()