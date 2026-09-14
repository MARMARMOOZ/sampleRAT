import socket
import time
import requests
from datetime import datetime


SERVER = "http://127.0.0.1:5000"


def execute_command(command):
    if command == "ping":
        return "pong"

    if command == "hostname":
        return socket.gethostname()

    if command == "time":
        return datetime.now().isoformat()

    return "command not allowed"


last_request_id = 0

while True:
    try:
        response = requests.get(
            SERVER + "/commands",
            timeout=10
        )

        data = response.json()

        request_id = data.get("id")
        command = data.get("command")

        if request_id is None:
            time.sleep(3)
            continue

        if request_id <= last_request_id:
            time.sleep(1)
            continue

        result = execute_command(command)

        requests.post(
            SERVER + "/response",
            json={
                "request_id": request_id,
                "response": result
            },
            timeout=10
        )

        last_request_id = request_id

    except requests.RequestException as e:
        print("Connection error:", e)
        time.sleep(5)

    except Exception as e:
        print("Error:", e)
        time.sleep(5)
