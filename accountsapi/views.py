from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from drf_yasg.utils import swagger_auto_schema

from .serializers import UserLoginSerializer, UserSerializer, RegistrationSerializer


# Create your views here.
class UserLoginApiView(GenericAPIView):
    serializer_class = UserLoginSerializer

    @swagger_auto_schema(
        responses={200: UserSerializer}, operation_summary="Api for Login user"
    )
    def post(self, request):
        serializer = UserLoginSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get("username")
        password = serializer.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            user_serializer = UserSerializer(user)
            return Response(
                {
                    "message": "Login Success",
                    "sucess": True,
                    "data": {"token": token.key, "user": user_serializer.data},
                },
                status=status.HTTP_200_OK,
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
                    "data": {"token": token.key, "user": serializer.data},
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
