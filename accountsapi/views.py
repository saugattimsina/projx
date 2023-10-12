from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from drf_yasg.utils import swagger_auto_schema

from user.models import UserKey

from .serializers import (
    UserLoginSerializer,
    UserSerializer,
    RegistrationSerializer,
    VerifyOTPSerializer,
    UserBinancyAPIKey,
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
        if user is not None:
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
