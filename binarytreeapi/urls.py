from django.urls import path
from .views import GetMYParentandChildren, GetUserRankApiView

urlpatterns = [
    path("my/child/parent/", GetMYParentandChildren.as_view()),
    path("my/rank/", GetUserRankApiView.as_view()),
]
