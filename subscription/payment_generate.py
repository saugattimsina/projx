import requests
import json
import pprint

url = "https://api-sandbox.nowpayments.io/v1/payment"


def get_payment_qr(price, username):
    payload = json.dumps(
        {
            "price_amount": price,
            # "price",
            "price_currency": "usd",
            "pay_currency": "btc",
            "ipn_callback_url": "https://42cb-27-34-76-169.ngrok-free.app/subscription/payment/",
            "order_id": username,
            # username,
            "order_description": "payment for subscription",
        }
    )
    headers = {
        "x-api-key": "4N917PW-13KMFS8-KCFRY6S-WE24V6X",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response.json()


# get_payment_qr(1,2)
