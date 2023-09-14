# Trading parameters
import ccxt

BINANCETN_API_KEY = "568fbe6822165f8feb172cd10ce0e1c39bd61f1102fab71d95fb9860eb94b226"
BINANCETN_API_SECRET = "cc8c83dd0013595db27a932f5eeda3f677beb5cd1e3c351b1e9b4b3c21a6364f"



symbol = "BNBUSDT"
trade_side = "buy"  # 'buy' or 'sell'
position_amount = 5
leverage = 10
trailing_stop_percent = 1
take_profit_percent = 2

# Initialize Binance exchange instance
exchange = ccxt.binance(
    {
        "apiKey": BINANCETN_API_KEY,
        "secret": BINANCETN_API_SECRET,
        "enableRateLimit": True,
        # "options": {"defaultType": "future", "defaultSubaccount": config.SU,},
        "options": {"defaultType": "future"},
    }
)
exchange.set_sandbox_mode(True)
