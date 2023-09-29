import requests
import json
import pprint
url = "https://api-sandbox.nowpayments.io/v1/payment"

def get_payment_qr(price,username):
  payload = json.dumps({
    "price_amount": price,
    # "price",
    "price_currency": "usd",
    "pay_currency": "btc",
    "ipn_callback_url": "https://b3c9-2403-3800-323a-b866-f262-9e3e-2a8a-207b.ngrok-free.app/subscription/payment/",
    "order_id": username,
      # username,
    "order_description": "payment for subscription",
  })
  headers = {
    'x-api-key': 'C73MTP8-QWG4EBT-HRWN2TQ-MYQ3K0S',
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  print(response.text)
  return response.json()


# get_payment_qr(1,2)