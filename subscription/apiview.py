from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import SubscriptionSerializer, SubscriptionDataSerializer
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Subscription, UserSubcription
from .services.create_address import create_wallet_address

# from rest_fremework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.pagination import PageNumberPagination

import qrcode
import base64
from io import BytesIO


class CreatePaymentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="API for getting payment QR code",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["subscription_id"],
            properties={
                "subscription_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID of the subscription for which to generate a QR code",
                )
            },
        ),
    )
    def post(self, request):
        subscription_id = request.data.get("subscription_id")
        if not subscription_id:
            return Response(
                {"error": "Subscription ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            subscription = Subscription.objects.get(id=subscription_id)
            user = request.user
            wallet_address = create_wallet_address(username=user.username)
            data = f"ethereum:{wallet_address}"
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill="black", back_color="white")
            img_buffer = BytesIO()
            img.save(img_buffer, format="PNG")
            img_buffer.seek(0)  # Move the buffer cursor to the start

            # Return the image directly as an HTTP response with image/png MIME type
            return HttpResponse(img_buffer, content_type="image/png")
        except Subscription.DoesNotExist:
            return Response(
                {"error": "Subscription not found", "success": False},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": str(e), "success": False}, status=status.HTTP_400_BAD_REQUEST
            )


class SubscriptionListView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionDataSerializer
    pagination_class = PageNumberPagination


class MySubscriptionListView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            subscriptions = (
                UserSubcription.objects.filter(user=user).order_by("-id").first()
            )
            serializer = SubscriptionDataSerializer(subscriptions.plan)
            return Response(
                data={
                    "subcription": serializer.data,
                    "start_date": subscriptions.start_date,
                    "end_date": subscriptions.end_date,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
