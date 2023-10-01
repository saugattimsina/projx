from django.urls import path
from .views import determine_rank_in_tree

urlpatterns = [path("tree/", determine_rank_in_tree, name="rank")]
