from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
import ccxt
from user.models import UserKey

from .models import TradeSignals,SignalFollowedBy,TradeSymbol

from .serializers import TradeHistorySerializer

from drf_yasg.utils import swagger_auto_schema


def get_open_orders(api_key,api_secret):
    symbol = 'XRPUSDT'  
    exchange = ccxt.binance(
    {
        "apiKey": api_key,
        "secret": api_secret,
        "enableRateLimit": True,
        "options": {"defaultType": "future"},
    })
    exchange.set_sandbox_mode(True)


    try:
        open_orders = exchange.fetch_open_orders(symbol=symbol)
        data = []
        if open_orders:
            for order in open_orders:
                # print(order)
                data.append({"order_id":order["id"],"status":order["status"],"type":order["type"],"side":order["side"],"price":order["price"],"amount":order["amount"]})
                # print(f"Order ID: {order['id']}, Status: {order['status']} ,Type: {order['type']}, Side: {order['side']}, Price: {order['price']}, Amount: {order['amount']}]")
            return {"data":data,"message":"open orders found"}
        else:
            return {"data":data,"message":"no open orders found"}
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"data":[],"message":"error occured please try again later"}

class OpenOrders(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        # print(request.user)
        user_key = UserKey.objects.filter(user=request.user).first()
        if user_key:
            data = get_open_orders(user_key.api_key,user_key.api_secret)
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"data":[],"message": "Update Your API key and secret"}, status=status.HTTP_204_NO_CONTENT)
        
def fetch_user_balance(api_key,api_secret):
    exchange = ccxt.binance(
    {
        "apiKey": api_key,
        "secret": api_secret,
        "enableRateLimit": True,
        "options": {"defaultType": "future"},
    })
    exchange.set_sandbox_mode(True)
    try:
        balance = exchange.fetchBalance()
    except Exception as e:
        return {"data":[],"message":"error occured please try again later"}
        # print(balance['total'])
    data = []
    for currency, info in balance.items():
        # total_balance += info['total']

        if currency == "USDT" or currency == "BTC" or currency == "ETH" or currency == "BNB" or currency=="USDC" or currency=="BUSD":
            # print(currency)
            # print(info['total'], info['used'], info['free'])
            data.append({"currency":currency,"total":info['total'],"used":info['used'],"free":info['free']})
    return {"data":data,"message":"balance check successfull"}
class ShowBalance(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user_key = UserKey.objects.filter(user=request.user).first()
        if user_key:
            data = fetch_user_balance(user_key.api_key,user_key.api_secret)
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"data":[],"message": "Update Your API key and secret"}, status=status.HTTP_204_NO_CONTENT)
        # return Response({"data":[],"message":"balance"},status=status.HTTP_200_OK)


def fetch_trade_history(api_key,api_secret,symbol):
    exchange = ccxt.binance(
    {
        "apiKey": api_key,
        "secret": api_secret,
        "enableRateLimit": True,
        "options": {"defaultType": "future"},
    })
    exchange.set_sandbox_mode(True)
    try:
        trades = exchange.fetch_my_trades(symbol=symbol)
    except Exception as e:
        return {"data":[],"message":"error occured please try again later"}
    history = []
    # Iterate through the trade history and print each trade

    if trades:
        print(trades)
        for trade in trades:
            print(f"Trade ID: {trade['id']}")
            print(f"Timestamp: {trade['timestamp']}")
            print(f"Price: {trade['price']}")
            print(f"Quantity: {trade['amount']}")
            print(f"Side: {trade['side']}")
            print(f"Fee: {trade['fee']}")
            print(f"---------------------")
            history.append({"trade_id":trade['id'],"price":trade['price'],"amount":trade[''],"timestamp":trade['timestamp'],"price":trade['price'],"quantity":trade['amount'],"side":trade['side'],"fee":trade['fee']})
        return {"data":history,"message":"trade history found"}
    else:
        return {"data":[],"message":"no trade history found"}


class TradeHistory(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TradeHistorySerializer


    @swagger_auto_schema(
        responses={200: TradeHistorySerializer}, operation_summary="test user history"
    )
    def get(self, request, format=None):
        serializer = self.serializer_class(data=request.data,context={'request':request})
        if serializer.is_valid():
            data =serializer.get_trade_from_date()
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"data":[],"message": serializer.errors},status=status.HTTP_400_BAD_REQUEST)


