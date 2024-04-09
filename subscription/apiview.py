from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import SubscriptionSerializer, SubscriptionDataSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Subscription, UserSubcription

# from rest_fremework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import PageNumberPagination


class CreatePaymentView(APIView):
    serializer_class = SubscriptionSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(operation_summary="Api for getting payment qr code")
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        payment_id = serializer.create_payment_custom(validated_data=request.data)
        return Response({"payment_id": payment_id}, status=status.HTTP_200_OK)


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
