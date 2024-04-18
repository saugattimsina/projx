from django.urls import path
from .apiview import ReferalIncomeHistoryAPIView, EarnningStatsApiView

urlpatterns = [
    path(
        "referal-income-history/",
        ReferalIncomeHistoryAPIView.as_view({"get": "list"}),
    ),
    path(
        "earning/stats/<int:user_id>/",
        EarnningStatsApiView.as_view(),
        name="earning_stats",
    ),
    path(
        "earning/stats/<int:user_id>/<str:starting_date>/<str:ending_date>/",
        EarnningStatsApiView.as_view(),
        name="earning_stats_date",
    ),
]
