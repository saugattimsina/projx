from django.urls import path

from .views import (
   TradeCreateView,TelegramWebhook
)

app_name = "signalbot"
urlpatterns = [
    path("createtrade", TradeCreateView.as_view(), name="create-trade"),
    path("telegram/<str:token>/", TelegramWebhook.as_view(), name="telegram_webhook")
  
]
