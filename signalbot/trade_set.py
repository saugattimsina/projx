# Trading parameters
import ccxt
from .models import SignalFollowedBy, Portfolio
import logging

logger = logging.getLogger("django.request")
# BINANCETN_API_KEY = "568fbe6822165f8feb172cd10ce0e1c39bd61f1102fab71d95fb9860eb94b226"
# BINANCETN_API_SECRET = "cc8c83dd0013595db27a932f5eeda3f677beb5cd1e3c351b1e9b4b3c21a6364f"


# symbol = "XRPUSDT"
trade_side = "buy"  # 'buy' or 'sell'
quantity = 100
# price = 0.4800
# stop_price= 0.45
# profit_price = 0.56

# leverage = 0
# trailing_stop_percent = 1
# take_profit_percent = 2
exchange = ccxt.binance(
    {
        "enableRateLimit": True,
        "options": {"defaultType": "future"},
    }
)
exchange.set_sandbox_mode(True)


def get_market_price_status(symbol):
    ticker = exchange.fetch_ticker(symbol)
    current_price = ticker["last"]
    print(current_price)
    return current_price


# def create_my_trade(signal_obj, user, userkey):

#     print(signal_obj.symbol.symbol)
#     symbol = signal_obj.symbol.symbol
#     price_now = get_market_price_status(symbol)

#     price = signal_obj.price
#     stop_price = signal_obj.stop_amount
#     # profit_price = signal_obj.take_profit_amount

#     if signal_obj.trade_type == "Buy/Long":
#         trade_side = "buy"
#     else:
#         trade_side = "sell"

#     print(trade_side)

#     """the trade could not be set in this condition"""
#     # if not price_now > stop_price:
#     #     print(price_now,stop_price)
#     #     print("price is not good")
#     #     return False

#     try:
#         exchange1 = ccxt.binance(
#             {
#                 "apiKey": userkey.api_key,
#                 "secret": userkey.api_secret,
#                 "enableRateLimit": True,
#                 # "options": {"defaultType": "future", "defaultSubaccount": config.SU,},
#                 "options": {"defaultType": "future"},
#             }
#         )
#         exchange1.set_sandbox_mode(True)
#     except Exception as e:
#         return "api key is not valid"
#     follower = SignalFollowedBy.objects.create(user=user, signal=signal_obj)
#     # try:
#     # help(exchange.create_order)
#     user_balance = 0
#     try:
#         balance = exchange1.fetchBalance()
#         for currency, info in balance.items():
#             if currency == "USDT":
#                 user_balance = info["free"]
#                 break
#     except Exception as e:
#         return "api key is not valid"
#     if user_balance < 20:
#         return "in sufficient balance"
#     balance_usable = user_balance * 0.9
#     quantity = balance_usable / price_now
#     print("trade lagne bela")

#     try:

#         create_order = exchange1.create_order(
#             symbol=symbol,
#             type="LIMIT",
#             side=trade_side,
#             amount=quantity,
#             price=price,
#         )
#         print("created order", create_order)

#     except Exception as e:
#         follower.is_cancelled = True
#         follower.save()
#         return "order could not be placed"
#     inverted_side = "sell" if trade_side == "buy" else "buy"

#     try:
#         stopLossParams = {"stopPrice": stop_price}
#         stopLossOrder = exchange1.create_order(
#             symbol, "STOP_MARKET", inverted_side, quantity, stop_price, stopLossParams
#         )
#         print(stopLossOrder)
#     except Exception as e:
#         print(e)
#         follower.is_cancelled = True
#         follower.save()
#         """need to cancel create orser if exixts"""
#         # exchange1.cancel_order(create_order['id'], symbol=symbol)
#         return "stop loss could not be placed"

#     for i in range(4):
#         # total_profits= 0
#         if signal_obj.amount_1 and signal_obj.percentage_1 and i == 0:
#             amount = signal_obj.amount_1
#             percentage = signal_obj.percentage_1
#         elif signal_obj.amount_2 and signal_obj.percentage_2 and i == 1:
#             amount = signal_obj.amount_2
#             percentage = signal_obj.percentage_2
#         elif signal_obj.amount_3 and signal_obj.percentage_3 and i == 2:
#             amount = signal_obj.amount_3
#             percentage = signal_obj.percentage_3
#         elif signal_obj.amount_4 and signal_obj.percentage_4 and i == 3:
#             amount = signal_obj.amount_4
#             percentage = signal_obj.percentage_4
#         else:
#             continue

#         """
#           here check the ampunt and amound has to be equal to quantiti
#         """
#         takeProfitParams = {"stopPrice": amount}
#         quantity_new = amount * percentage / 100
#         try:
#             takeProfitOrder = exchange1.create_order(
#                 symbol,
#                 "TAKE_PROFIT_MARKET",
#                 inverted_side,
#                 quantity_new,
#                 price,
#                 takeProfitParams,
#             )
#             print(takeProfitOrder)
#         except Exception as e:
#             print(e)
#             """need to cancel create orser if exixts"""
#             # exchange1.cancel_order(create_order['id'], symbol=symbol)
#             # exchange1.cancel_order(stopLossOrder['id'], symbol=symbol)
#             follower.is_cancelled = True
#             follower.save()
#             return "take profit could not be placed"

#     # yo part milaina baki
#     # Portfolio.objects.create(user=user,symbol=symbol,quantity=quantity,entry_price=price,stop_price=stop_price,take_profit_price=profit_price)
#     # exchange1.close()


def create_my_trade(signal_obj, user, userkey):
    symbol = signal_obj.symbol.symbol
    price_now = get_market_price_status(symbol)
    price = signal_obj.price
    stop_price = signal_obj.stop_amount
    trade_side = "buy" if signal_obj.trade_type == "Buy/Long" else "sell"
    additional_params = {}
    if price < round((price_now - price_now * 0.005), 4):
        print(f"price can't be less than {round((price_now - price_now * 0.005), 4)}")
        logging.info(
            f"price can't be less than {round((price_now - price_now * 0.005), 4)}"
        )
        return f"price can't be less than {round((price_now - price_now * 0.005), 4)}"
    elif price > round((price_now + price_now * 0.005), 4):
        print(f"price can't be higher than {round((price_now + price_now * 0.005), 4)}")
        logging.info(
            f"price can't be higher than {round((price_now + price_now * 0.005), 4)}"
        )
        return f"price can't be higher than {round((price_now + price_now * 0.005), 4)}"

    if trade_side == "buy" and price < stop_price:
        return f"Stop loss cannot be higher than price"
    elif trade_side == "sell" and price < signal_obj.amount:
        return f"Take profit cannot be less the price"

    try:
        exchange1 = ccxt.binance(
            {
                "apiKey": userkey.api_key,
                "secret": userkey.api_secret,
                "enableRateLimit": True,
                "options": {"defaultType": "future"},
            }
        )
        exchange1.set_sandbox_mode(True)
    except Exception as e:
        logging.info(f"error setting sandbox mode {str(e)}")
        print(str(e))
        return str(e)

    follower = SignalFollowedBy.objects.create(user=user, signal=signal_obj)

    user_balance = 0

    try:
        balance = exchange1.fetch_balance()
        user_balance = balance["free"]["USDT"]
    except Exception as e:
        print(str(e))
        return str(e)

    balance_usable = user_balance * 0.9

    quantity = balance_usable / price_now

    if quantity * price < 5:
        print("you must buy minimum $5 worth of Coins")
        logging.info("you must buy minimum $5 worth of Coins")
        return "In sufficient balance"

    try:
        print(symbol, trade_side, quantity, price)
        create_order = exchange1.create_order(
            symbol=symbol,
            type="LIMIT",
            side=trade_side,
            amount=quantity,
            price=price,
        )
        print("created order")
        logging.info("created order")
    except Exception as e:
        logging.info(str(e))
        follower.is_cancelled = True
        follower.save()
        logging.info("failed to create order")
        return "order could not be placed"

    inverted_side = "sell" if trade_side == "buy" else "buy"

    try:
        additional_params["stopPrice"] = stop_price
        stop_loss_order = exchange1.create_order(
            symbol=symbol,
            type="STOP_MARKET",
            side=inverted_side,
            amount=quantity,
            price=stop_price,
            params=additional_params,
        )
        print("stop_loss_order created")
        logging.info("stop_loss_order created")
    except Exception as e:
        print(e)
        logging.info(e)
        follower.is_cancelled = True
        follower.save()
        return "stop loss could not be placed"

    for i in range(4):
        if signal_obj.amount_1 and signal_obj.percentage_1 and i == 0:
            amount = signal_obj.amount_1
            percentage = signal_obj.percentage_1
        elif signal_obj.amount_2 and signal_obj.percentage_2 and i == 1:
            amount = signal_obj.amount_2
            percentage = signal_obj.percentage_2
        elif signal_obj.amount_3 and signal_obj.percentage_3 and i == 2:
            amount = signal_obj.amount_3
            percentage = signal_obj.percentage_3
        elif signal_obj.amount_4 and signal_obj.percentage_4 and i == 3:
            amount = signal_obj.amount_4
            percentage = signal_obj.percentage_4
        else:
            continue

        additional_params["stopPrice"] = amount
        quantity_new = quantity - (quantity * (1 - (1 * percentage / 100)))
        try:
            print(symbol, inverted_side, quantity_new, amount, additional_params)
            take_profit_order = exchange1.create_order(
                symbol=symbol,
                type="TAKE_PROFIT_MARKET",
                side=inverted_side,
                amount=quantity_new,
                price=amount,
                params=additional_params,
            )
            print("take_profit_order created")
            logging.info("take_profit_order created")
        except Exception as e:
            print(e)
            logging.info(e)
            follower.is_cancelled = True
            follower.save()
            return "take profit could not be placed"


def all_symbols():
    exchange = ccxt.binance(
        {
            "rateLimit": 2000,  # Adjust this rate limit as needed
            "enableRateLimit": True,
            "options": {
                "defaultType": "future",
            },
        }
    )

    # Fetch all available markets (symbols) for Binance Futures
    markets = exchange.fetch_markets()

    # Print the list of trading symbols
    for market in markets:
        print(market["symbol"])


# all_symbols()
