from django.urls import path

from .views import PaymentWebhook, SubcriptionPaymentcallback

from .apiview import (
    CreatePaymentView,
    SubscriptionListView,
    MySubscriptionListView,
)

app_name = "subscription"
urlpatterns = [
    path("payment/", PaymentWebhook.as_view(), name="telegram_webhook"),
    path(
        "payment/callback/<int:user_id>/",
        SubcriptionPaymentcallback.as_view(),
        name="subcription_payment_callback",
    ),
    path("create/payment/", CreatePaymentView.as_view(), name="create_payment"),
    path(
        "get-subscriptions-package/",
        SubscriptionListView.as_view({"get": "list"}),
        name="get_sub",
    ),
    path(
        "get-my-subscriptions-package/",
        MySubscriptionListView.as_view(),
        name="get_my_sub",
    ),
]
