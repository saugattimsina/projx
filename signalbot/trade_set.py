# Trading parameters
import ccxt

BINANCETN_API_KEY = "568fbe6822165f8feb172cd10ce0e1c39bd61f1102fab71d95fb9860eb94b226"
BINANCETN_API_SECRET = "cc8c83dd0013595db27a932f5eeda3f677beb5cd1e3c351b1e9b4b3c21a6364f"



# symbol = "XRPUSDT"
trade_side = "buy"  # 'buy' or 'sell'
quantity = 100
# price = 0.4800
# stop_price= 0.45
# profit_price = 0.56

# leverage = 0
# trailing_stop_percent = 1
# take_profit_percent = 2

# Initialize Binance exchange instance
def create_my_trade(signal_obj,user,userkey):
    symbol = signal_obj.symbol
    price = signal_obj.price
    stop_price = signal_obj.stop_amount
    profit_price = signal_obj.take_profit_amount
    exchange = ccxt.binance(
        {
            "apiKey": userkey.api_key,
            "secret": userkey.api_secret,
            "enableRateLimit": True,
            # "options": {"defaultType": "future", "defaultSubaccount": config.SU,},
            "options": {"defaultType": "future"},
        }
    )
    exchange.set_sandbox_mode(True)

    # try:
    # help(exchange.create_order)
    try:
        create_order = exchange.create_order(
            symbol=symbol,
            type="LIMIT",
            side=trade_side,
            amount=quantity,
            price=price,
        )
        print(create_order)
        inverted_side = 'sell'

        stopLossParams = {'stopPrice': stop_price}
        stopLossOrder = exchange.create_order(symbol, 'STOP_MARKET', inverted_side, quantity, price, stopLossParams)
        print(stopLossOrder)

        takeProfitParams = {'stopPrice': profit_price}
        takeProfitOrder = exchange.create_order(symbol, 'TAKE_PROFIT_MARKET', inverted_side, quantity, price, takeProfitParams)
        print(takeProfitOrder)

    except Exception as e:
        print(e)



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
