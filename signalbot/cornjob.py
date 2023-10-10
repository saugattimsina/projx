import ccxt

from user.models import UserKey
from signalbot.models import TradeHistory,TradeSymbol,TradeSignals,SignalFollowedBy,Portfolio

from datetime import date
from celery import shared_task

@shared_task
def get_my_trade_history(UserKey):
    exchange = ccxt.binance({
    'apiKey': UserKey.api_key,
    'secret': UserKey.api_secret,
    "options": {"defaultType": "future"},

    })
    exchange.set_sandbox_mode(True)
    today = date.today()
    trades_today = Portfolio.objects.filter(created_on__date=today)
    users_on_date = trades_today.values_list('user', flat=True).distinct()
    # start_time = exchange.parse8601 ('2023-10-05T00:00:00')
    # now = exchange.parse8601 ('2023-10-10T00:00:00')

    for user in users_on_date:
        print(user)

    
    