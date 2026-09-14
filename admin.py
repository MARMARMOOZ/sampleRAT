import time
import requests


SERVER = "http://127.0.0.1:5000"


while True:
    command = input("command --> ").strip()

    if not command:
        continue

    try:
        response = requests.post(
            SERVER + "/admin",
            json={
                "command": command
            },
            timeout=10
        )

        data = response.json()

        if response.status_code != 201:
            print("Error:", data)
            continue

        request_id = data["id"]

        print("Request ID:", request_id)
        print("Waiting for response...")

        while True:
            response = requests.get(
                SERVER + f"/responses/{request_id}",
                timeout=10
            )

            data = response.json()

            if data.get("status") != "pending":
                print(data["response"])
                break

            time.sleep(2)

    except requests.RequestException as e:
        print("Connection error:", e)
