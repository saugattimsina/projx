from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from .serializers import SubscriptionSerializer
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Subscription, UserSubcription, UserWalletAddress
from .services.create_address import create_wallet_address

# from rest_fremework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.pagination import PageNumberPagination


class CreateSubscriptionsPaymentView(GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def post(self, request, format=None):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                subscription_time = serializer.validated_data["subscription_time"]
                if subscription_time < 1:
                    return Response(
                        {"message": "subscription time must be greater than 0"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    user = request.user
                    subscription = Subscription.objects.all().order_by("-id").first()
                    wallet_address = create_wallet_address(username=user.username)
                    UserWalletAddress.objects.create(
                        user=user,
                        wallet_address=wallet_address,
                        subscription=subscription,
                    )
                    return Response(
                        {
                            "data": {
                                "wallet_address": wallet_address,
                                "amount": subscription.price,
                            },
                            "success": True,
                        },
                        status=status.HTTP_200_OK,
                    )
            else:
                return Response(
                    {"message": serializer.errors, "success": False},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Subscription.DoesNotExist:
            return Response(
                {"error": "Subscription not found", "success": False},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": str(e), "success": False}, status=status.HTTP_400_BAD_REQUEST
            )


# class CreatePaymentView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     @swagger_auto_schema(
#         operation_summary="API for getting bitcoin addresses",
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             required=["subscription_id"],
#             properties={
#                 "subscription_id": openapi.Schema(
#                     type=openapi.TYPE_INTEGER,
#                     description="ID of the subscription",
#                 )
#             },
#         ),
#     )
#     def post(self, request):
#         subscription_id = request.data.get("subscription_id")
#         if not subscription_id:
#             return Response(
#                 {"error": "Subscription ID is required"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         try:
#             subscription = Subscription.objects.get(id=subscription_id)
#             if subscription.package_type == "paid":
#                 user = request.user
#                 wallet_address = create_wallet_address(username=user.username)
#                 UserWalletAddress.objects.create(
#                     user=user, wallet_address=wallet_address, subscription=subscription
#                 )
#                 return Response(
#                     {
#                         "wallet_address": wallet_address,
#                         "amount": subscription.price,
#                     },
#                     status=status.HTTP_200_OK,
#                 )
#         except Subscription.DoesNotExist:
#             return Response(
#                 {"error": "Subscription not found", "success": False},
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#         except Exception as e:
#             return Response(
#                 {"error": str(e), "success": False}, status=status.HTTP_400_BAD_REQUEST
#             )


# class SubscriptionListView(ReadOnlyModelViewSet):
#     queryset = Subscription.objects.all()
#     serializer_class = SubscriptionDataSerializer
#     pagination_class = PageNumberPagination


# class MySubscriptionListView(APIView):
#     authentication_classes = [TokenAuthentication]

#     def get(self, request, *args, **kwargs):
#         try:
#             user = request.user
#             subscriptions = UserSubcription.objects.filter(user=user).order_by("-id")
#             if subscriptions.exists():
#                 serializer = SubscriptionDataSerializer(subscriptions.first().plan)
#                 return Response(
#                     data={
#                         "subscription": serializer.data,
#                         "start_date": subscriptions.start_date,
#                         "end_date": subscriptions.end_date,
#                     },
#                     status=status.HTTP_200_OK,
#                 )
#             else:
#                 return Response(
#                     {"message": "No subscription found", "success": False},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
