# Trading parameters
import ccxt
from .models import SignalFollowedBy

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
    })
exchange.set_sandbox_mode(True)
def get_market_price_status(symbol):
    ticker = exchange.fetch_ticker(symbol)
    current_price = ticker['last']
    print(current_price)
    return current_price


def create_my_trade(signal_obj,user,userkey):
    
    symbol = signal_obj.symbol
    price_now = get_market_price_status()

    price = signal_obj.price
    stop_price = signal_obj.stop_amount
    profit_price = signal_obj.take_profit_amount

    """the trade could not be set in this condition"""
    if not price_now > stop_price:
        print(price_now,stop_price)
        print("price is not good")
        return False


    exchange1 = ccxt.binance(
        {
            "apiKey": userkey.api_key,
            "secret": userkey.api_secret,
            "enableRateLimit": True,
            # "options": {"defaultType": "future", "defaultSubaccount": config.SU,},
            "options": {"defaultType": "future"},
        }
    )
    exchange1.set_sandbox_mode(True)

    SignalFollowedBy.objects.create(user=user,signal=signal_obj)
    # try:
    # help(exchange.create_order)
    
    try:
        create_order = exchange1.create_order(
                symbol=symbol,
                type="LIMIT",
                side=trade_side,
                amount=quantity,
                price=price,
            )
       
    except Exception as e:
        return "order could not be placed"
        inverted_side = 'sell'

        stopLossParams = {'stopPrice': stop_price}
        stopLossOrder = exchange.create_order(symbol, 'STOP_MARKET', inverted_side, quantity, price, stopLossParams)
        print(stopLossOrder)

        takeProfitParams = {'stopPrice': profit_price}
        takeProfitOrder = exchange.create_order(symbol, 'TAKE_PROFIT_MARKET', inverted_side, quantity, price, takeProfitParams)
        print(takeProfitOrder)
        exchange.close()

 
        exchange.close()



# create_stoploss_order = exchange.create_stop_loss_order(
#     symbol=symbol,
#     amount=quantity,
#     price=stop_price,
#     )


# x = exchange.create_limit_sell_order(
#     symbol=symbol,
#     type="STOP_LOSS",
#     side=trade_side,
#     amount=quantity,
#     price=0.52,
#     params={"stopPrice": stop_price},
# )


# order_info = exchange.fetch_order(order_id, 'BTC/USDT')




def all_symbols():
    exchange = ccxt.binance({
        'rateLimit': 2000,  # Adjust this rate limit as needed
        'enableRateLimit': True,
        'options': {
            'defaultType': 'future',
        }
    })

    # Fetch all available markets (symbols) for Binance Futures
    markets = exchange.fetch_markets()

    # Print the list of trading symbols
    for market in markets:
        print(market['symbol'])
# all_symbols()