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
    PasswordResetConfirmAPIView,
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
    # path("send/email/otp/<int:user_id>/", SendOTPForPasswordForget.as_view()),
    # path("verify/email/otp/<int:user_id>/", ValidateEmailOTP.as_view()),
    path("change/password/", ChangeUserPasswordAPIView.as_view()),
    path("password-reset/", ResetPasswordAPIView.as_view()),
    path("password-reset-confirm/", PasswordResetConfirmAPIView.as_view()),
]
