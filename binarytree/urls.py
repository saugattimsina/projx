from django.urls import path
from .views import treeview


app_name = "tree"
urlpatterns = [
    path("showtree/", treeview, name="tree")
]
