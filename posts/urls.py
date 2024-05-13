from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .apiview import PostViewSet, PublicPostViewSet
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)


urlpatterns = [
    path("web/", PostListView.as_view(), name="post_list"),
    path("web/post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("web/post/add/", PostCreateView.as_view(), name="post_add"),
    path("web/post/<int:pk>/edit/", PostUpdateView.as_view(), name="post_edit"),
    path("web/post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path("post/", PostViewSet.as_view({"get": "list", "post": "create"})),
    path("post/public/", PublicPostViewSet.as_view({"get": "list"})),
    path("post/public/<int:pk>/", PublicPostViewSet.as_view({"get": "retrieve"})),
    path(
        "post/<int:pk>/",
        PostViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
    ),
]
