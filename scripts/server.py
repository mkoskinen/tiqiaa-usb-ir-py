#!/usr/bin/env python3
"""Simple HTTP server for controlling Mitsubishi AC via Tiqiaa USB IR."""

import os
import subprocess
import sys
from http.server import HTTPServer, ThreadingHTTPServer, BaseHTTPRequestHandler

PORT = 8080
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
IR_DIR = os.path.join(REPO_DIR, "ir")
TIQIAA = os.path.join(REPO_DIR, "tiqiaa_usb_ir.py")

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
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            buttons = ""
            for t in TEMPS:
                buttons += (
                    f'<p><a href="/on/{t}">'
                    f'<button style="font-size:2em;padding:0.5em 1em">Cool {t}</button>'
                    f'</a></p>\n'
                )
            html = (
                '<html><body style="font-family:sans-serif;text-align:center;padding:2em">'
                '<h1>Mitsubishi AC</h1>'
                f'{buttons}'
                '<p><a href="/off">'
                '<button style="font-size:2em;padding:0.5em 1em;background:#c33;color:#fff">OFF</button>'
                '</a></p>'
                '</body></html>'
            )
            self.wfile.write(html.encode())

        elif self.path.startswith("/on/"):
            try:
                temp = int(self.path.split("/")[-1])
                if temp not in TEMPS:
                    raise ValueError
            except ValueError:
                self.send_error(400, f"Invalid temp. Use one of: {TEMPS}")
                return
            ok = send_ir(f"cool_on_{temp}.ir")
            self.send_response(302 if ok else 500)
            self.send_header("Location", "/")
            self.end_headers()

        elif self.path == "/off":
            ok = send_ir("off.ir")
            self.send_response(302 if ok else 500)
            self.send_header("Location", "/")
            self.end_headers()

        else:
            self.send_error(404)

    def log_message(self, format, *args):
        print(f"{self.client_address[0]} - {args[0]}")


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"Listening on http://0.0.0.0:{PORT}")
    server.serve_forever()
