import requests

from projx.settings import (
    EXTERNAL_API_URL,
    EXTERNAL_API_PASSWORD,
    EXTERNAL_API_USERNAME,
)
from .get_token import get_api_token
import json


def realease_token_in_address(userwalletaddress):
    try:
        auth_token = get_api_token()
        url = f"{EXTERNAL_API_URL}/tokenrelease"
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json",
        }
        data = {"WalletAddress": userwalletaddress}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        if response.status_code == 200:
            data = response.json()
            return True
    except Exception as e:
        return None
