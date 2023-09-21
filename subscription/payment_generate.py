import requests
import json
import pprint
url = "https://api-sandbox.nowpayments.io/v1/payment"

payload = json.dumps({
  "price_amount": 3999.5,
  "price_currency": "usd",
  "pay_currency": "btc",
  "ipn_callback_url": "https://a6a0-2403-3800-323a-a4f4-30e3-d790-c075-f6a1.ngrok-free.app/subscription/payment/",
  "order_id": "RGDBP-21314",
  "order_description": "Apple Macbook Pro 2019 x 1"
})
headers = {
  'x-api-key': 'C73MTP8-QWG4EBT-HRWN2TQ-MYQ3K0S',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

pprint.pprint(response.text)
