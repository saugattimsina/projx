from django.urls import path

from .views import (
   TradeCreateView,
   TelegramWebhook,
   TradeSignalHistory,
   DisplaySignalFollowers
)

app_name = "signalbot"
urlpatterns = [
    path("createtrade", TradeCreateView.as_view(), name="create-trade"),
    path("signal-history",TradeSignalHistory.as_view(),name="signal-history"),
    path('displaysignalfollowers/<int:signal_id>',DisplaySignalFollowers.as_view(),name='displaysignalfollowers'),
    path("telegram/<str:token>/", TelegramWebhook.as_view(), name="telegram_webhook")
]
