from django.urls import path

from .views import (
   PaymentWebhook,

)

from .apiview import (
    CreatePaymentView

)

app_name = "subscription"
urlpatterns = [

    path("payment/", PaymentWebhook.as_view(), name="telegram_webhook"),
    path('create/payment/', CreatePaymentView.as_view(), name='create_payment'),
]
