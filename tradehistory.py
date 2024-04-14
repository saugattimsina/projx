import ccxt  # noqa: E402
import os
import django

# Set the DJANGO_SETTINGS_MODULE to your project's settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projx.settings")

# Initialize Django
django.setup()

from signalbot.models import TradeHistory
from user.models import User

api_key = "568fbe6822165f8feb172cd10ce0e1c39bd61f1102fab71d95fb9860eb94b226"
api_secret = "cc8c83dd0013595db27a932f5eeda3f677beb5cd1e3c351b1e9b4b3c21a6364f"

exchange = ccxt.binance(
    {
        "apiKey": api_key,
        "secret": api_secret,
        "options": {"defaultType": "future"},
        # 'options': {
        #     'defaultType': 'spot', // spot, future, margin
        # },
    }
)
exchange.set_sandbox_mode(True)


exchange.load_markets()

# exchange.verbose = True  # uncomment for debugging

symbol = "XRP/USDT"
day = 24 * 60 * 60 * 1000
start_time = exchange.parse8601("2023-10-05T00:00:00")
now = exchange.parse8601("2023-10-10T00:00:00")

all_trades = []

while start_time < now:

    print("------------------------------------------------------------------")
    print("Fetching trades from", exchange.iso8601(start_time))
    end_time = start_time + day

    trades = exchange.fetch_my_trades(
        symbol,
        start_time,
        None,
        {
            "endTime": end_time,
        },
    )
    print(trades)
    if len(trades):
        last_trade = trades[len(trades) - 1]
        start_time = last_trade["timestamp"] + 1
        all_trades = all_trades + trades
    else:
        start_time = end_time

print("Fetched", len(all_trades), "trades")
for i in range(0, len(all_trades)):
    trade = all_trades[i]
    print(
        i,
        trade["id"],
        trade["datetime"],
        trade["amount"],
        trade["price"],
        trade["side"],
        trade["info"]["realizedPnl"],
        trade["fee"],
    )
    trade_history_instance = TradeHistory.objects.create(
        user=User.objects.get(username="admin"),
        trade_id=trade["id"],
        symbol=trade["info"]["symbol"],
        amount=trade["price"],
        price=trade["amount"],
        trade_side=trade["side"],
        profit_loss=trade["info"]["realizedPnl"],
        trade_fee=trade["fee"]["cost"],
        fee_currency=trade["fee"]["currency"],
        created_on=trade["datetime"],
    )
