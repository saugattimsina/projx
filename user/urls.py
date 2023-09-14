from django.urls import path

from .views import (
    GroupList,
    change_user_password,
    user_detail_view,
    user_redirect_view,
    user_update_view,
    GroupView,
    ListUsersView,
    GroupEditView,
    GroupDeleteView,
    UserEditView,
    UserCreateView,
    UserDeleteView,
    change_password_view
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("group",GroupView.as_view(),name="group"),
    path("group-list",GroupList.as_view(),name="group-list"),
    path("list",ListUsersView.as_view(),name="user_list"),
    path('createuser/',view=UserCreateView.as_view(),name="user_create"),
    path('editgroup/<str:pk>/',view=GroupEditView.as_view(),name="editgroup"),
    path('deletegroup/<str:pk>/',view=GroupDeleteView.as_view(),name="deletegroup"),
    path('edit/<str:pk>/',view=UserEditView.as_view(),name="edituser"),
    path('deleteuser/<str:pk>/',view=UserDeleteView.as_view(),name="deleteuser"),
    path('change_password/',view= change_password_view,name='change_password'),
    path('change_user_password/<int:id>',change_user_password,name='change_user_pwd'),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
