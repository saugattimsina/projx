import requests
from projx.settings import (
    EXTERNAL_API_URL,
    EXTERNAL_API_PASSWORD,
    EXTERNAL_API_USERNAME,
)


def get_api_token():
    try:
        url = f"{EXTERNAL_API_URL}/gettoken"

        username = EXTERNAL_API_USERNAME
        password = EXTERNAL_API_PASSWORD

        params = {username: username, password: password}

        response = requests.get(url, params=params)
        response.raise_for_status()
        if response.status_code == 200:
            data = response.json()
            token = data["data"]
            return token
        else:
            return None
    except Exception as e:
        return None
