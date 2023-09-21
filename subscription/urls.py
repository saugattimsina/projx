from django.urls import path

from .views import (
   PaymentWebhook,

)

app_name = "subscription"
urlpatterns = [

    path("payment/", PaymentWebhook.as_view(), name="telegram_webhook")
]
