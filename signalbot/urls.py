from django.urls import path

from .views import (
    TradeCreateView,
    TelegramWebhook,
    TradeSignalHistory,
    DisplaySignalFollowers,
    ShowPairs,
    ADDPairs,
    pair_info,
    #    ShowUserOrders
)
from .apiview import OpenOrders, ShowBalance, TradeHistoryView, ShowPositions

app_name = "signalbot"
urlpatterns = [
    path("createtrade", TradeCreateView.as_view(), name="create-trade"),
    path("signal-history", TradeSignalHistory.as_view(), name="signal-history"),
    path(
        "displaysignalfollowers/<int:signal_id>",
        DisplaySignalFollowers.as_view(),
        name="displaysignalfollowers",
    ),
    path("show/pairs/", ShowPairs.as_view(), name="show-pairs"),
    path("create/pairs/", ADDPairs, name="create-pairs"),
    path("pairs/info/", pair_info, name="get-pair-info"),
    # path('show-user-orders/',ShowUserOrders.as_view(),name='show-user-orders'),
    path("telegram/<str:token>/", TelegramWebhook.as_view(), name="telegram_webhook"),
    # api view
    path("openorders/", OpenOrders.as_view(), name="openorders"),
    path("tradehistory/", TradeHistoryView.as_view(), name="closedorders"),
    path(
        "tradehistory/<str:starting_date>/<str:ending_date>/",
        TradeHistoryView.as_view(),
        name="closedorders-by-date",
    ),
    path("balance/", ShowBalance.as_view(), name="balance-show"),
    path("positions/", ShowPositions.as_view(), name="positions-show"),
]
