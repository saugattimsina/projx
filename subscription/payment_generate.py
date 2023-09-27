import requests
import json
import pprint
url = "https://api.nowpayments.io/v1/payment"

def get_payment_qr(price,username):
  payload = json.dumps({
    "price_amount": 10,
    # "price",
    "price_currency": "usd",
    "pay_currency": "btc",
    "ipn_callback_url": "https://411a-2403-3800-323a-b25e-8150-b8af-4261-dfe5.ngrok-free.app/subscription/payment/",
    "order_id": "ram",
      # username,
    "order_description": "payment for subscription",
  })
  headers = {
    'x-api-key': '6E4MP38-0BQM52M-QYQJ8N5-Z4XE2VC',
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  print(response.text)
  return response.json()


# get_payment_qr(1,2)