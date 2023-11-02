from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from user.models import UserKey
from accountsapi.utils import generate_otp, send_otp_email

from .serializers import (
    UserLoginSerializer,
    UserSerializer,
    RegistrationSerializer,
    VerifyOTPSerializer,
    UserBinancyAPIKey,
    ChangePasswordSerializer,
)

User = get_user_model()


# Create your views here.
class UserLoginApiView(GenericAPIView):
    serializer_class = UserLoginSerializer

    @swagger_auto_schema(
        responses={200: UserLoginSerializer}, operation_summary="Api for Login user"
    )
    def post(self, request, format=None):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)
        token.delete()
        token = Token.objects.create(user=token.user)
        if user is not None:
            if user.is_connected_to_authunticator:
                return Response(
                    {
                        "success": True,
                        "data": {
                            "user_id": user.id,
                            # "username": user.username,
                        },
                        "message": "Login Successful. Proceed to 2FA",
                    },
                    status=200,
                )
            else:
                return Response(
                    {
                        "success": True,
                        "data": {
                            "user": {
                                "user_id": user.id,
                                # "username": user.username,
                                # "image": user.image.path if user.image else None,
                                # "is_client": user.is_client,
                                "qr_code": user.qr_code.url,
                            },
                        },
                    },
                    status=200,
                )
        else:
            return Response(
                {
                    "message": "Invaid Username or Password",
                    "sucess": False,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )


class UserRegistrationApiView(GenericAPIView):
    serializer_class = RegistrationSerializer

    @swagger_auto_schema(operation_summary="Api for registration of the user")
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "message": "Registration Success. Proceed to 2FA",
                    "sucess": True,
                    "data": {
                        # "token": token.key,
                        "user": {
                            "user_id": user.id,
                            # "username": user.username,
                            # "image": user.image.path if user.image else None,
                            # "is_client": user.is_client,
                            "qr_code": user.qr_code.url,
                        },
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "message": serializer.errors,
                "sucess": False,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class VerityOTPView(GenericAPIView):
    serializer_class = VerifyOTPSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data["user_id"]
            user = User.objects.filter(id=user_id).first()
            if not user.is_connected_to_authunticator:
                user.is_connected_to_authunticator = True
                user.save()
            login_info: dict = serializer.save()
            return Response(
                {
                    "success": True,
                    "data": login_info,
                    "message": "2fa verification sucess",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "message": serializer.errors.get("non_field_errors", [""])[0],
                    "success": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class ApiForUserBinanceKey(ModelViewSet):
    serializer_class = UserBinancyAPIKey
    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(operation_summary="Api for saving user binance api key")
    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = UserBinancyAPIKey(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            key = UserKey.objects.get(user=user, is_active=True)
            key.is_active = False
            key.save()
        except:
            print("no previous key")
        serializer.save(user=user)
        return Response(
            {"message": "save key successfully", "success": True},
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(operation_summary="Api for updating user binance api key")
    def update(self, request, *args, **kwargs):
        user = self.request.user
        try:
            key = UserKey.objects.get(user=user, is_active=True)
        except:
            return Response(
                {"message": "User have no  key", "success": False},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = UserBinancyAPIKey(key, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Updated key successfully", "success": True},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": serializer.errors, "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogoutApiView(APIView):
    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(
        operation_summary="Api for logging user out and expire user token"
    )
    def post(self, request):
        user = self.request.user
        token = Token.objects.get(user=user)
        token.delete()
        token = Token.objects.create(user=token.user)
        return Response(
            {"message": "Logout success", "success": True},
            status=status.HTTP_200_OK,
        )


class SendOTPForPasswordForget(APIView):
    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(
        operation_summary="Api for sending otp to email for password forget"
    )
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            otp = generate_otp()
            user.email_otp = otp
            user.save()
            email = user.email
            send_otp_email(email, otp)
            return Response(
                {"message": "OTP has been sent to your email", "success": True},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response({"message": "User not found", "success": False}, status=404)


class ValidateEmailOTP(APIView):
    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "otp": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                ),
            },
        ),
        operation_summary="Api for validating email otp",
    )
    def post(self, request, user_id):
        otp = request.data.get("otp")
        try:
            user = User.objects.get(id=user_id)
            if user.email_otp == otp:
                user.email_otp = None  # Reset the OTP field after successful validation
                user.save()
                return Response(
                    {"message": "Invalid OTP.", "success": False},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                return Response(
                    {"message": "Procced to password change", "success": True},
                    status=status.HTTP_200_OK,
                )
        except User.DoesNotExist:
            return Response({"message": "User not found", "success": False}, status=404)


class ResetPasswordAPIView(APIView):
    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "new_password": openapi.Schema(
                    type=openapi.TYPE_STRING,
                ),
            },
        ),
        operation_summary="Api for Changing password",
    )
    def post(self, request, user_id):
        new_password = request.data.get("new_password")
        try:
            user = User.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()
            return Response(
                {"message": "Password changed successfully", "success": True},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response({"message": "User not found", "success": False}, status=404)


class ChangeUserPasswordAPIView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(operation_summary="Api for updating user password")
    def post(self, request, user_id):
        serializer = ChangePasswordSerializer(data=request.data)
        try:
            user = User.objects.get(id=user_id)
            if serializer.is_valid():
                if user.check_password(serializer.data.get("old_password")):
                    user.set_password(serializer.data.get("new_password"))
                    user.save()
                    return Response(
                        {"message": "Password changed successfully."},
                        status=status.HTTP_200_OK,
                    )
                return Response(
                    {"error": "Incorrect old password."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "User not found", "success": False}, status=404)
