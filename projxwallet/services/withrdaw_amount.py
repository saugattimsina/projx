import requests

from projx.settings import (
    EXTERNAL_API_URL,
    EXTERNAL_API_PASSWORD,
    EXTERNAL_API_USERNAME,
    FROM_ADDRESS,
    ADDRESS_KEY,
)
from subscription.services.get_token import get_api_token
import json


def withdraw_amount_from_wallet(address, amount):
    auth_token = get_api_token()
    url = f"{EXTERNAL_API_URL}/ProcessWithdrawal"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }
    data = {
        "FromAddress": FROM_ADDRESS,
        "AddressKey": ADDRESS_KEY,
        "ToAddress": address,
        "Amount": amount,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    if response.status_code == 200:
        data = response.json()
        return True
    else:
        return None
