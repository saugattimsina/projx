import requests
from .get_token import get_api_token
from projx.settings import EXTERNAL_API_URL


def create_wallet_address(username):
    try:
        auth_token = get_api_token()
        url = f"{EXTERNAL_API_URL}/createaddress"
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json",
        }
        data = {username: username}
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        if response.status_code == 200:
            data = response.json()
            address = data["data"]
            return address
        else:
            return None
    except Exception as e:
        return None
