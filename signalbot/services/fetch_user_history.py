import requests
from datetime import datetime, timezone
import ccxt

from ..models import Portfolio, TradeHistory
from user.models import User, UserKey

import logging

logger = logging.getLogger("django.request")


def create_user_new_history(user):
    """
    Creates a new user's trade history
    """
    try:
        current_datetime_utc = datetime.now(timezone.utc)
        midnight_datetime_utc = current_datetime_utc.replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        midnight_timestamp_milliseconds = int(midnight_datetime_utc.timestamp() * 1000)
        user_key = UserKey.objects.get(user=user, is_active=True)
        exchange = ccxt.binance(
            {
                "apiKey": user_key.api_key,
                "secret": user_key.api_secret,
                "options": {"defaultType": "future"},
            }
        )
        exchange.set_sandbox_mode(True)
        symbols_used = (
            Portfolio.objects.filter(user=user)
            .values_list("symbol__symbol", flat=True)
            .distinct()
        )
        print(symbols_used)
        for symbol in symbols_used:
            print(symbol)
            trades = exchange.fetch_my_trades(
                symbol=symbol, since=midnight_timestamp_milliseconds
            )
            for trade in trades:
                try:
                    trade_history_instance = TradeHistory.objects.filter(
                        user=user, trade_id=trade["id"]
                    )
                    if trade_history_instance.exists():
                        pass
                    else:
                        trade_history_instance = TradeHistory.objects.create(
                            user=user,
                            trade_id=trade["id"],
                            symbol=trade["info"]["symbol"],
                            amount=trade["price"],
                            price=trade["amount"],
                            trade_side=trade["side"],
                            profit_loss=trade["info"]["realizedPnl"],
                            trade_fee=trade["fee"]["cost"],
                            fee_currency=trade["fee"]["currency"],
                            created_on=trade["datetime"],
                            timestamp=trade["timestamp"],
                        )
                except Exception as e:
                    print(e)
                    logger.error(f"error creating TradeHistory object {str(e)}")
                    pass

    except Exception as e:
        print(e)
        logger.error(f"error creating user TradeHistory {str(e)}")
        pass
