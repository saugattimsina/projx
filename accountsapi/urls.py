from django.urls import path

from .views import (
    UserLoginApiView,
    UserRegistrationApiView,
    VerityOTPView,
    ApiForUserBinanceKey,
    LogoutApiView,
    SendOTPForPasswordForget,
    ValidateEmailOTP,
    ResetPasswordAPIView,
    ChangeUserPasswordAPIView,
)

urlpatterns = [
    # user Api
    path("login/", UserLoginApiView.as_view()),
    path("logout/", LogoutApiView.as_view()),
    path("registrations/", UserRegistrationApiView.as_view()),
    path("verify/otp/", VerityOTPView.as_view()),
    path("add/key/", ApiForUserBinanceKey.as_view({"post": "create"})),
    path("update/key/", ApiForUserBinanceKey.as_view({"put": "update"})),
    path("send/email/otp/<int:user_id>/", SendOTPForPasswordForget.as_view()),
    path("verify/email/otp/<int:user_id>/", ValidateEmailOTP.as_view()),
    path("change/password/<int:user_id>/", ChangeUserPasswordAPIView.as_view()),
    path("reset/password/<int:user_id>/", ResetPasswordAPIView.as_view()),
]
