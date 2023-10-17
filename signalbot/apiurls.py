from django.urls import path
from .apiview import ReferalIncomeHistoryAPIView

urlpatterns = [
    path(
        "referal-income-history/<int:user_id>",
        ReferalIncomeHistoryAPIView.as_view({"get": "list"}),
    ),
]
