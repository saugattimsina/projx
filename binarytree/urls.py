from django.urls import path
from .views import treeview, determine_rank_in_tree, determineparents


app_name = "tree"
urlpatterns = [
    path("showtree/", treeview, name="tree"),
    path("tree/", determine_rank_in_tree, name="rank"),
    path("binarypay/", determineparents, name="binarypay"),
]
