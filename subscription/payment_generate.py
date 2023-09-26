import requests
import json
import pprint
url = "https://api-sandbox.nowpayments.io/v1/payment"

def get_payment_qr(price,username):
  payload = json.dumps({
    "price_amount": price,
    "price_currency": "usd",
    "pay_currency": "btc",
    "ipn_callback_url": "http://96e9-2403-3800-323a-a782-41f0-7543-69d0-df68.ngrok-free.app/subscription/payment/",
    "order_id": username,
    "order_description": "payment for subscription",
  })
  headers = {
    'x-api-key': 'C73MTP8-QWG4EBT-HRWN2TQ-MYQ3K0S',
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  return response.json()
