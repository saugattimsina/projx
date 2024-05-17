import requests

from projx.settings import (
    EXTERNAL_API_URL,
    EXTERNAL_API_PASSWORD,
    EXTERNAL_API_USERNAME,
)
from .get_token import get_api_token
import json
from ..models import UserSubcription, UserSubPaymentHistory
from .release_token import realease_token_in_address
from django.utils import timezone


def get_address_balance(address, user, subcription):
    try:
        username = user.username
        auth_token = get_api_token()
        url = f"{EXTERNAL_API_URL}/getbalance"
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json",
        }
        data = {"WalletAddress": address, "Username": username}
        response = requests.get(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        if response.status_code == 200:
            data = response.json()
            balance = data["data"]
            has_partial_payment = True
            remaining_amount = float(subcription.price) - float(balance)
            if float(balance) >= subcription.price:
                remaining_amount = 0
                has_partial_payment = False
                UserSubcription.objects.create(user=user, plan=subcription)
            UserSubPaymentHistory.objects.create(
                user=user,
                subscription=subcription,
                amount=balance,
                remaining_amount=remaining_amount,
                has_partial_payment=has_partial_payment,
                date_transaction=timezone.now(),
            )
            realease_token_in_address(userwalletaddress=address)
            return balance
        else:
            print(response.json())
            return None
    except Exception as e:
        print(e)
        return None
