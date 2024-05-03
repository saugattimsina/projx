from ..models import Order
from user.models import User, UserKey
import ccxt


def updateOrder():
    orders = Order.objects.all()

    for order in orders:
        user = order.user
        user_keys = UserKey.objects.get(user=user)
        order_id = order.order_id
        symbol = order.symbol.symbol
        exchange = ccxt.binance(
            {
                "apiKey": user_keys.api_key,
                "secret": user_keys.api_secret,
                "enableRateLimit": True,
                "options": {"defaultType": "future"},
            }
        )

        exchange.set_sandbox_mode(True)

        fetch_order = exchange.fetch_order(id=order_id, symbol=symbol)

        if fetch_order["info"]["status"] == "FILLED":
            order.filled = True

        order.filled_quantity = fetch_order["filled"]
        order.remaining_quantity = fetch_order["remaining"]
        order.executed_date_time = fetch_order["datetime"]
        order.avg_price = round(fetch_order["average"], 2)

        order.save()
