# from rest_framework.serializers import ModelSerializer,Serializer

from rest_framework import serializers

from datetime import datetime
from .models import (
    TradeSignals,
    SignalFollowedBy,
    TradeSymbol,
    TradeHistory,
    Portfolio,
    ReferalWithdrawlHistory,
    ReferalIncome,
)
from user.models import User, UserKey
import ccxt
from django.utils import timezone

# def fetch_trade_history(api_key,api_secret,symbol,exchange):

#     try:
#         trades = exchange.fetch_my_trades(symbol=symbol)
#     except Exception as e:
#         return {"data":[],"message":"error occured please try again later"}
#     history = []
#     # Iterate through the trade history and print each trade

#     if trades:
#         print(trades)
#         for trade in trades:
#             print(f"Trade ID: {trade['id']}")
#             print(f"Timestamp: {trade['timestamp']}")
#             print(f"Price: {trade['price']}")
#             print(f"Quantity: {trade['amount']}")
#             print(f"Side: {trade['side']}")
#             print(f"Fee: {trade['fee']}")
#             print(f"---------------------")
#             history.append({"trade_id":trade['id'],"price":trade['price'],"amount":trade[''],"timestamp":trade['timestamp'],"price":trade['price'],"quantity":trade['amount'],"side":trade['side'],"fee":trade['fee']})
#         return {"data":history,"message":"trade history found"}
#     else:
#         return {"data":[],"message":"no trade history found"}


class TradeHistorySerializer(serializers.Serializer):
    from_date = serializers.DateField(required=True)
    to_date = serializers.DateField(required=True)

    def get_trade_from_date(self):
        # Define the start and end date range
        start_date = self.validated_data["from_date"]
        end_date = self.validated_data["to_date"]

        # Convert the date objects to Unix timestamps
        history = []
        since = (
            int(datetime.combine(start_date, datetime.min.time()).timestamp()) * 1000
        )  # Multiply by 1000 to convert to milliseconds
        until = int(datetime.combine(end_date, datetime.max.time()).timestamp()) * 1000
        print(self.context["request"].user)
        unique_signals = SignalFollowedBy.objects.filter(
            user=self.context["request"].user,
            created_on__range=(start_date, end_date),
        )
        print(unique_signals)
        symbols = []
        for signals in unique_signals:
            signal = signals.signal.symbol.symbol
            if not signal in symbols:
                symbols.append(signal)

        if symbols:
            key = UserKey.objects.filter(user=self.context["request"].user)
            if key:
                print(key[0].api_key)
                print(key[0].api_secret)
                exchange = ccxt.binance(
                    {
                        "apiKey": key[0].api_key,
                        "secret": key[0].api_secret,
                        "enableRateLimit": True,
                        "options": {"defaultType": "future"},
                    }
                )
                exchange.set_sandbox_mode(True)
                # print(exchange)
            else:
                return {"data": [], "message": "no api key found"}
            print(symbols)
            for i in symbols:
                print(i)
                try:
                    trades = exchange.fetch_my_trades(symbol=i)
                    print(trades)
                    if trades:
                        for trade in trades:
                            history.append(
                                {
                                    "trade_id": trade["id"],
                                    "price": trade["price"],
                                    "amount": trade["amount"],
                                    "timestamp": trade["timestamp"],
                                    "side": trade["side"],
                                    "fee": trade["fee"],
                                }
                            )
                except Exception as e:
                    print(e)
                    return {
                        "data": [],
                        "message": "error occured please try again later",
                    }
        else:
            return {"data": [], "message": "no trade history found"}
        return {"data": history, "message": "trade history found"}


class TradesHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeHistory
        fields = "__all__"


class ReferalIncomeHistorySerializer(serializers.ModelSerializer):
    refered_by = serializers.StringRelatedField()
    refered_user = serializers.StringRelatedField()
    money_allocated_to = serializers.StringRelatedField()

    class Meta:
        model = ReferalIncome
        fields = [
            "refered_by",
            "refered_user",
            "money_allocated_to",
            "amount",
            "created_on",
        ]
