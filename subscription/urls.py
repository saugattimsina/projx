from django.urls import path

from .apiview import (
    CreateSubscriptionsPaymentView,
)

app_name = "subscription"
urlpatterns = [
    path(
        "create/payment/",
        CreateSubscriptionsPaymentView.as_view(),
        name="create_payment",
    ),
    # path(
    #     "get-subscriptions-package/",
    #     SubscriptionListView.as_view({"get": "list"}),
    #     name="get_sub",
    # ),
    # path(
    #     "get-my-subscriptions-package/",
    #     MySubscriptionListView.as_view(),
    #     name="get_my_sub",
    # ),
]
