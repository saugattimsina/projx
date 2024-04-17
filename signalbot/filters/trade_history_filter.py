import django_filters
from django.db import models

from ..models import TradeHistory


class TradeHistoryFilter(django_filters.FilterSet):
    order = django_filters.OrderingFilter(fields=(("created_on", "-created_on"),))

    search = django_filters.CharFilter(
        method="filter_search",
        label="Search",
    )

    class Meta:
        model = TradeHistory
        fields = {
            "trade_id": ["exact"],
            "symbol": ["exact"],
            "amount": ["exact", "gte", "lte"],
            "price": ["exact", "gte", "lte"],
            "created_on": ["exact", "gte", "lte"],
            "trade_side": ["exact"],
        }

    def filter_search(self, queryset, name, value):
        return queryset.filter(models.Q(symbol__icontains=value))
