#!/usr/bin/env python3

"""Simple HTTP server for controlling Mitsubishi AC via Tiqiaa USB IR."""

import os
import subprocess
import sys
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

PORT = 8080
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
IR_DIR = os.path.join(REPO_DIR, "ir")
TIQIAA = os.path.join(REPO_DIR, "tiqiaa_usb_ir.py")
HTML_FILE = os.path.join(SCRIPT_DIR, "index.html")

TEMPS = [20, 21, 22, 23, 24]


def send_ir(filename):
    path = os.path.join(IR_DIR, filename)
    result = subprocess.run(
        [sys.executable, TIQIAA, "-s", path],
        capture_output=True, text=True
    )
    return result.returncode == 0


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            try:
                with open(HTML_FILE, "rb") as f:
                    body = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            except OSError:
                self.send_error(500, "index.html not found")

        elif self.path.startswith("/on/"):
            try:
                temp = int(self.path.split("/")[-1])
                if temp not in TEMPS:
                    raise ValueError
            except ValueError:
                self.send_error(400, f"Invalid temp. Use one of: {TEMPS}")
                return
            ok = send_ir(f"cool_on_{temp}.ir")
            self.send_response(200 if ok else 500)
            self.end_headers()

        elif self.path == "/off":
            ok = send_ir("off.ir")
            self.send_response(200 if ok else 500)
            self.end_headers()

        else:
            self.send_error(404)

    def log_message(self, format, *args):
        print(f"{self.client_address[0]} - {args[0]}")


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"Listening on http://0.0.0.0:{PORT}")
    server.serve_forever()
