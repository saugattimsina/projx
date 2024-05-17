from django.shortcuts import render
from .models import ProjxWallet, ProjxWalletHistory
from subscription.services.create_address import create_wallet_address
from .serializers import ProjxWalletSerializer
from .services.withrdaw_amount import withdraw_amount_from_wallet


# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework import status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class FetchProjxWalletBalanceView(GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            wallet = ProjxWallet.objects.filter(user=user).first()
            if wallet:
                return Response(
                    {
                        "data": {
                            "balance": wallet.amount,
                        },
                        "success": True,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                wallet = ProjxWallet.objects.create(user=user)
                return Response(
                    {
                        "data": {
                            "balance": wallet.amount,
                        },
                        "success": True,
                    },
                    status=status.HTTP_200_OK,
                )
        except Exception as e:
            return Response(
                data={
                    "message": str(e),
                    "success": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class DepositProjxWallet(GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            wallet_address = create_wallet_address(username=user.username)
            ProjxWalletHistory.objects.create(
                amount=0,
                wallet_address=wallet_address,
                transaction_type=ProjxWalletHistory.TRANSACTION_TYPE.DEPOSIT,
                status=ProjxWalletHistory.STATUS_CHOICES.PENDING,
            )
            return Response(
                {
                    "data": {
                        "wallet_address": wallet_address,
                    },
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                data={
                    "message": str(e),
                    "success": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class WithdrawProjxWallet(GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjxWalletSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            user_projx_wallet = ProjxWallet.objects.get(user=user)
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                wallet_address = serializer.validated_data["wallet_address"]
                amount = serializer.validated_data["amount"]
                if user_projx_wallet.amount < amount or user_projx_wallet.amount == 0:
                    return Response(
                        {"message": "Insufficient balance", "success": False},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                elif amount < 1:
                    return Response(
                        {"message": "Amount must be greater than 0", "success": False},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                withdraw = withdraw_amount_from_wallet(
                    address=wallet_address, amount=amount
                )
                if withdraw:
                    ProjxWalletHistory.objects.create(
                        amount=amount,
                        wallet_address=wallet_address,
                        transaction_type=ProjxWalletHistory.TRANSACTION_TYPE.WITHDRAW,
                        status=ProjxWalletHistory.STATUS_CHOICES.SUCCESS,
                    )
                    user_projx_wallet.amount = user_projx_wallet.amount - amount
                    user_projx_wallet.save()
                    return Response(
                        {
                            "message": "Transaction is successfully",
                            "success": False,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    ProjxWalletHistory.objects.create(
                        amount=amount,
                        wallet_address=wallet_address,
                        transaction_type=ProjxWalletHistory.TRANSACTION_TYPE.WITHDRAW,
                        status=ProjxWalletHistory.STATUS_CHOICES.FAILED,
                    )
                    return Response(
                        {
                            "message": "Transaction is failed",
                            "success": False,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"message": serializer.errors, "success": False},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                data={
                    "message": str(e),
                    "success": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
