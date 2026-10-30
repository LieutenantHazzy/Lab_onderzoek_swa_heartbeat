#!/usr/bin/env python3
import json
import socket
import time
from urllib import request
from urllib.error import URLError

# Instellingen
SERVER_URL = "http://127.0.0.1:9000/beat"  # Verander naar IP van de server als je tussen machines test
INTERVAL = 5  # Seconden tussen heartbeats
CLIENT_ID = socket.gethostname()

def send_heartbeat():
    payload = {
        "hostname": CLIENT_ID,
        "ts": time.time(),
        "status": "alive"
    }

    data = json.dumps(payload).encode("utf-8")

    try:
        req = request.Request(
            SERVER_URL,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with request.urlopen(req, timeout=3) as response:
            if response.status == 200:
                print(f"[{time.strftime('%H:%M:%S')}] Heartbeat verzonden -> OK")
            else:
                print(f"[{time.strftime('%H:%M:%S')}] Heartbeat verzonden -> {response.status}")

    except URLError as e:
        print(f"[{time.strftime('%H:%M:%S')}] Kan geen verbinding maken: {e.reason}")
    except TimeoutError:
        print(f"[{time.strftime('%H:%M:%S')}] Timeout bij verzenden heartbeat")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Onverwachte fout: {e}")

if __name__ == "__main__":
    print(f"Heartbeat client gestart -> {SERVER_URL}")
    print(f"Verzendt elke {INTERVAL} seconden. Druk op Ctrl+C om te stoppen.\n")

    try:
        while True:
            send_heartbeat()
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nClient gestopt.")
