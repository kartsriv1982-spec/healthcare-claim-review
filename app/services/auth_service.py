import requests

AUTH_SERVICE_URL = "http://localhost:8081"


def login(username, password):

    response = requests.post(
        f"{AUTH_SERVICE_URL}/api/v1/auth/login",
        json={
            "username": username,
            "password": password
        }
    )

    response.raise_for_status()

    return response.json()