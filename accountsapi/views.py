from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from drf_yasg.utils import swagger_auto_schema

from .serializers import (
    UserLoginSerializer,
    UserSerializer,
    RegistrationSerializer,
    VerifyOTPSerializer,
)

User = get_user_model()


# Create your views here.
class UserLoginApiView(GenericAPIView):
    serializer_class = UserLoginSerializer

    @swagger_auto_schema(
        responses={200: UserSerializer}, operation_summary="Api for Login user"
    )
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user is not None:
            return Response(
                {
                    "success": True,
                    "data": {
                        "user_id": user.id,
                        "username": user.username,
                        "qr_code": user.qr_code.url,
                    },
                    "message": "Login Successful. Proceed to 2FA",
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
                    "message": "Registration Success",
                    "sucess": True,
                    "data": {
                        "token": token.key,
                        "user": {
                            "user_id": user.id,
                            "username": user.username,
                            "image": user.image.path,
                            "is_client": user.is_client,
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
            user_id = serializer.validated_data("user_id")
            user = User.objects.filter(id=user_id).first()
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
