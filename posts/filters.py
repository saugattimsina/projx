import django_filters
from django.db import models

from .models import Post


class PostFilter(django_filters.FilterSet):
    order = django_filters.OrderingFilter(fields=(("created_on", "-created_on"),))

    search = django_filters.CharFilter(
        method="filter_search",
        label="Search",
    )

    class Meta:
        models = Post
        fields = {
            "title": ["icontains"],
            "slug": ["exact"],
            "created_on": ["gte", "lte", "exact"],
            "updated_at": ["gte", "lte", "exact"],
            "status": ["exact"],
            "category": ["exact"],
        }

    def filter_search(self, queryset, name, value):
        return queryset.filter(models.Q(title__icontains=value))
