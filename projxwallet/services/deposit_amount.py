import requests

from projx.settings import (
    EXTERNAL_API_URL,
    EXTERNAL_API_PASSWORD,
    EXTERNAL_API_USERNAME,
    FROM_ADDRESS,
    ADDRESS_KEY,
)
from subscription.services.get_token import get_api_token
from subscription.services.release_token import realease_token_in_address
import json
from ..models import ProjxWallet, ProjxWalletHistory


def deposit_amount_address(address, projx_wallet_history_obj):
    try:
        username = projx_wallet_history_obj.user.username
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
            realease_token_in_address(userwalletaddress=address)
            wallet = ProjxWallet.objects.get(user=projx_wallet_history_obj.user)
            wallet.amount += float(balance)
            wallet.save()
            projx_wallet_history_obj.amount = float(balance)
            status = ProjxWalletHistory.STATUS_CHOICES.SUCCESS
            projx_wallet_history_obj.save()
            return balance
        else:
            print(response.json())
            return None
    except Exception as e:
        print(e)
        return None
