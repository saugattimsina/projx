from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView

import ccxt
from django.db.models import Sum
from user.models import UserKey

from .models import (
    TradeSignals,
    SignalFollowedBy,
    TradeSymbol,
    Portfolio,
    TradeHistory,
    ReferalIncome,
    ReferalWithdrawlHistory,
    BinaryIncome,
)
from user.models import User

from .serializers import (
    TradeHistorySerializer,
    TradesHistorySerializer,
    ReferalIncomeHistorySerializer,
)

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from drf_yasg.inspectors import PaginatorInspector

from django.utils import timezone
from datetime import datetime, timedelta
from django.utils.dateparse import parse_date

three_days_ago = datetime.now() - timedelta(days=3)


def get_open_orders(user, api_key, api_secret, symbol):
    """
    need to get all symbols from database
    """
    # symbol = 'XRPUSDT'
    # SignalFollowedBy.objects.filter(user=user).values_list("signal__symbol__symbol", flat=True).distinct()

    # print(symbols)
    exchange = ccxt.binance(
        {
            "apiKey": api_key,
            "secret": api_secret,
            "enableRateLimit": True,
            "options": {"defaultType": "future"},
        }
    )
    exchange.set_sandbox_mode(True)

    data = []

    try:
        open_orders = exchange.fetch_open_orders(symbol=symbol)
        if open_orders:
            for order in open_orders:
                print(order)
                # print(order)
                data.append(
                    {
                        "symbol": symbol,
                        "order_id": order["id"],
                        "status": order["status"],
                        "type": order["type"],
                        "side": order["side"],
                        "price": order["price"],
                        "amount": order["amount"],
                    }
                )
                # print(f"Order ID: {order['id']}, Status: {order['status']} ,Type: {order['type']}, Side: {order['side']}, Price: {order['price']}, Amount: {order['amount']}]")
            return data
        else:
            return {"data": data, "message": "no open orders found"}
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"data": [], "message": "error occured please try again later"}


class OpenOrders(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # print(request.user)
        user_key = UserKey.objects.filter(user=request.user).first()
        three_days_ago = datetime.now() - timedelta(days=30)
        if user_key:
            symbols = (
                SignalFollowedBy.objects.filter(
                    user=user_key.user, created_on__gte=three_days_ago
                )
                .values_list("signal__symbol__symbol", flat=True)
                .distinct()
            )
            datas = []
            for symbol in symbols:
                data = get_open_orders(
                    user_key.user, user_key.api_key, user_key.api_secret, symbol
                )
                datas.append(data)
            # datas["succes"] = True

            return Response({"data": datas, "success": True}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"data": [], "message": "Update Your API key and secret"},
                status=status.HTTP_204_NO_CONTENT,
            )


def fetch_user_balance(api_key, api_secret):
    exchange = ccxt.binance(
        {
            "apiKey": api_key,
            "secret": api_secret,
            "enableRateLimit": True,
            "options": {"defaultType": "future"},
        }
    )
    exchange.set_sandbox_mode(True)
    try:
        balance = exchange.fetchBalance()
    except Exception as e:
        return {"data": [], "message": "error occured please try again later"}
        # print(balance['total'])
    data = []
    for currency, info in balance.items():
        # total_balance += info['total']

        if currency == "USDT":
            # print(currency)
            # print(info['total'], info['used'], info['free'])
            data.append(
                {
                    "currency": currency,
                    "total": info["total"],
                    "used": info["used"],
                    "free": info["free"],
                }
            )
            break
    return {"data": data, "message": "balance check successfull"}


class ShowBalance(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_key = UserKey.objects.filter(user=request.user).first()
        if user_key:
            data = fetch_user_balance(user_key.api_key, user_key.api_secret)
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"data": [], "message": "Update Your API key and secret"},
                status=status.HTTP_204_NO_CONTENT,
            )
        # return Response({"data":[],"message":"balance"},status=status.HTTP_200_OK)


def fetch_trade_history(api_key, api_secret, symbol):
    exchange = ccxt.binance(
        {
            "apiKey": api_key,
            "secret": api_secret,
            "enableRateLimit": True,
            "options": {"defaultType": "future"},
        }
    )
    exchange.set_sandbox_mode(True)
    try:
        trades = exchange.fetch_my_trades(symbol=symbol)
    except Exception as e:
        return {"data": [], "message": "error occured please try again later"}
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
            history.append(
                {
                    "trade_id": trade["id"],
                    "price": trade["price"],
                    "amount": trade[""],
                    "timestamp": trade["timestamp"],
                    "price": trade["price"],
                    "quantity": trade["amount"],
                    "side": trade["side"],
                    "fee": trade["fee"],
                }
            )
        return {"data": history, "message": "trade history found"}
    else:
        return {"data": [], "message": "no trade history found"}


def create_new_history(user):
    threshold_time = timezone.now() - timezone.timedelta(minutes=30)
    # Portfolio.objects.filter(user=self.context['request'].user)
    # user = self.context['request'].user
    recent_portfolios = Portfolio.objects.filter(
        created_on__gte=threshold_time, user=user
    )
    if recent_portfolios:
        user_key = UserKey.objects.filter(user=user)
        if user_key.exists():
            exchange = ccxt.binance(
                {
                    "apiKey": user_key.api_key,
                    "secret": user_key.api_secret,
                    "options": {"defaultType": "future"},
                }
            )
            exchange.set_sandbox_mode(True)
            # symbol = []
            for trade in recent_portfolios:
                trades_in_time_range = exchange.fetch_my_trades(trade.symbol.symbol)
                if trades_in_time_range:
                    for trade in trades_in_time_range:
                        try:
                            trade_history_instance = TradeHistory.objects.create(
                                user=user,
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
                            continue
                else:
                    return True

        else:
            return False, "no api key found"
    else:
        return True


# class TradeHistoryView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     @swagger_auto_schema(
#         responses={200: TradesHistorySerializer()},
#         operation_summary="Test user history",
#     )
#     def get(self, request, format=None):
#         # Create trade history data
#         trade_data = create_new_history(request.user)
#         if trade_data == False:
#             return Response(
#                 {"data": [], "message": "Update Your API key and secret"},
#                 status=status.HTTP_204_NO_CONTENT,
#             )
#         # Serialize the trade_data using TradesHistorySerializer
#         serializer = TradesHistorySerializer(
#             data=TradeHistory.objects.filter(user=request.user), many=True
#         )
#         serializer.is_valid()


#         return Response(serializer.data, status=200)


class TradeHistoryView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TradesHistorySerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return TradeHistory.objects.filter(user=self.request.user).order_by(
            "created_on"
        )

    @swagger_auto_schema(
        operation_summary=" Get list of Trade history",
        paginator_class=PaginatorInspector,
        manual_parameters=[
            # Add pagination parameters to the manual_parameters list
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="Page number",
                type=openapi.TYPE_INTEGER,
            ),
        ],
    )
    def get(self, request, starting_date=None, ending_date=None, *args, **kwargs):
        trade_data = create_new_history(request.user)
        if trade_data == False:
            return Response(
                {"data": [], "message": "Update Your API key and secret"},
                status=status.HTTP_204_NO_CONTENT,
            )
        if starting_date and ending_date:
            start_date = parse_date(starting_date)
            print(start_date)
            end_date = parse_date(ending_date)
            query = TradeHistory.objects.filter(
                user=self.request.user,
                created_on__date__gte=start_date,
                created_on__date__lte=end_date,
            ).order_by("-created_on")
        else:
            query = TradeHistory.objects.filter(user=self.request.user).order_by(
                "-created_on"
            )
        serializer = self.get_serializer(query, many=True)
        queryset = self.filter_queryset(query)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(
                {
                    "message": "user trade history",
                    "sucess": True,
                    "data": serializer.data,
                },
            )
        return Response(serializer.data)


class ReferalIncomeHistoryAPIView(ModelViewSet):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = ReferalIncomeHistorySerializer

    def list(self, request, user_id):
        user = User.objects.filter(id=user_id).first()
        if user:
            serializer = ReferalIncomeHistorySerializer(
                data=ReferalIncome.objects.filter(money_allocated_to=user), many=True
            )
            serializer.is_valid()
            return Response(
                {
                    "data": serializer.data,
                    "message": "User income history",
                    "sucess": True,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"data": [], "message": "no user found", "sucess": False},
                status=status.HTTP_204_NO_CONTENT,
            )


class EarnningStatsApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="shows earning status",
    )
    def get(self, request, user_id, starting_date=None, ending_date=None, format=None):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"data": [], "message": "No user found", "success": False},
                status=status.HTTP_404_NOT_FOUND,
            )

        if starting_date and ending_date:
            start_date = parse_date(starting_date)
            print(start_date)
            end_date = parse_date(ending_date)
            total_referal_income = ReferalIncome.objects.filter(
                money_allocated_to=user,
                created_on__date__gte=start_date,
                created_on__date__lte=end_date,
            ).aggregate(total_amount=Sum("amount"))["total_amount"]
            total_matrix_income = BinaryIncome.objects.filter(
                money_allocated_to=user,
                created_on__date__gte=start_date,
                created_on__date__lte=end_date,
            ).aggregate(total_amount=Sum("amount"))["total_amount"]
            return Response(
                {
                    "data": {
                        "total_referal_income": total_referal_income,
                        "total_matrix_income": total_matrix_income,
                    },
                    "message": "Earning stats fetched",
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )
        else:
            total_referal_income = ReferalIncome.objects.filter(
                money_allocated_to=user
            ).aggregate(total_amount=Sum("amount"))["total_amount"]
            total_matrix_income = BinaryIncome.objects.filter(
                money_allocated_to=user
            ).aggregate(total_amount=Sum("amount"))["total_amount"]
            return Response(
                {
                    "data": {
                        "total_referal_income": total_referal_income,
                        "total_matrix_income": total_matrix_income,
                    },
                    "message": "Earning stats fetched",
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )


# def get_positions(key,secret):
#     balance = exchange.fetch_balance()


class ShowPositions(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: TradesHistorySerializer()},
        operation_summary="Test user history",
    )
    def post(self, request):
        user_key = UserKey.objects.filter(user=request.user).first()
        if user_key:
            exchange = ccxt.binance(
                {
                    "apiKey": user_key.api_key,
                    "secret": user_key.api_secret,
                    "enableRateLimit": True,
                    "options": {"defaultType": "future"},
                }
            )
            exchange.set_sandbox_mode(True)
            balance = exchange.fetch_balance()
            positions = balance["info"]["positions"]
            user_positions = []
            # print(positions)
            if positions:
                for position in positions:
                    if float(position["initialMargin"]) != 0:
                        print(position)
                        user_positions.append(position)
            if user_positions:
                return Response(
                    {
                        "data": user_positions,
                        "message": "positions found",
                        "success": True,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"data": [], "message": "no positions found", "success": False},
                    status=status.HTTP_204_NO_CONTENT,
                )
        else:
            return Response(
                {"data": [], "message": "no api key found", "success": False},
                status=status.HTTP_204_NO_CONTENT,
            )
