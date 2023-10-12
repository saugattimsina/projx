from django.urls import path

from .views import (
   PaymentWebhook,

)

from .apiview import (
    CreatePaymentView,
    SubscriptionListView,

)

app_name = "subscription"
urlpatterns = [

    path("payment/", PaymentWebhook.as_view(), name="telegram_webhook"),
    path('create/payment/', CreatePaymentView.as_view(), name='create_payment'),
    path("get-subscriptions-package/", SubscriptionListView.as_view(), name="get_sub"),
]
