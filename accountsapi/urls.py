from django.urls import path

from .views import UserLoginApiView, UserRegistrationApiView


urlpatterns = [
    # user Api
    path("login/", UserLoginApiView.as_view()),
    path("registrations/", UserRegistrationApiView.as_view()),
]
