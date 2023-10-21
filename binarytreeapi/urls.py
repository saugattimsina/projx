from django.urls import path
from .views import GetMYParentandChildren, GetUserRankApiView

urlpatterns = [
    path("my/child/parent/<int:user_id>/", GetMYParentandChildren.as_view()),
    path("my/rank/<int:user_id>/", GetUserRankApiView.as_view()),
]
