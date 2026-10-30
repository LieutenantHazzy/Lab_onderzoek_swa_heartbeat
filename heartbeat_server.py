#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import json

HOST = "0.0.0.0"
PORT = 9000

class HeartbeatHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/beat":
            try:
                content_length = int(self.headers.get("Content-Length", "0"))
                body = self.rfile.read(content_length).decode("utf-8")

                try:
                    data = json.loads(body)
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] HEARTBEAT ontvangen van {data.get('hostname', 'onbekend')} | ts: {data.get('ts')}")
                except json.JSONDecodeError:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] HEARTBEAT ontvangen (raw): {body}")

                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"OK")

            except Exception as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Fout bij verwerken: {e}")
                self.send_response(500)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *args):
        pass

if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), HeartbeatHandler)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Heartbeat server draait op http://{HOST}:{PORT}/beat")
    print("Wachten on heartbeats...\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer gestop.")
        server.server_close()
