from django.urls import path

from .views import (
    UserLoginApiView,
    UserRegistrationApiView,
    VerityOTPView,
    ApiForUserBinanceKey,
)


urlpatterns = [
    # user Api
    path("login/", UserLoginApiView.as_view()),
    path("registrations/", UserRegistrationApiView.as_view()),
    path("verify/otp/", VerityOTPView.as_view()),
    path("add/key/", ApiForUserBinanceKey.as_view({"post": "create"})),
    path("update/key/", ApiForUserBinanceKey.as_view({"put": "update"})),
]
