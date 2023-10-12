import ccxt

from user.models import UserKey
from signalbot.models import (
    TradeHistory,
    TradeSymbol,
    TradeSignals,
    SignalFollowedBy,
    Portfolio,
)

from datetime import datetime, timedelta
from django.utils import timezone
from celery import shared_task


@shared_task
def get_trade_history():
    thirty_min_ago = timezone.now() - timedelta(minutes=30)
    """
    yaha issue aucca ki bichar garau
    """

    trades_now = Portfolio.objects.filter(created_on__gte=thirty_min_ago)
    for user in trades_now:
        print(user.user)
        
        user_key = UserKey.objects.get(user=user.user, is_active=True)
        symbol = user.symbol.symbol
        exchange = ccxt.binance(
            {
                "apiKey": user_key.api_key,
                "secret": user_key.api_secret,
                "options": {"defaultType": "future"},
            }
        )
        exchange.set_sandbox_mode(True)
        start_timestamp = int(
            datetime.timestamp(datetime.now(timezone.utc) - timedelta(minutes=15))
            * 1000
        )
        end_timestamp = int(datetime.timestamp(datetime.now(timezone.utc)) * 1000)
        all_trades = exchange.fetch_my_trades(symbol)
        trades_in_time_range = [
            trade
            for trade in all_trades
            if start_timestamp <= trade["timestamp"]
            and trade["timestamp"] <= end_timestamp
        ]
        for trade in trades_in_time_range:
            try:
                trade_history_instance = TradeHistory.objects.create(
                    user=user.user,
                    trade_id=trade["id"],
                    symbol=trade["info"]["symbol"],
                    amount=trade["price"],
                    price=trade["amount"],
                    trade_side=trade["side"],
                    profit_loss=trade["realizedPnl"],
                    trade_fee=trade["fee"]["cost"],
                    fee_currency=trade["fee"]["currency"],
                    created_on=trade["datetime"],
                )
            except:
                print("trade already created")
