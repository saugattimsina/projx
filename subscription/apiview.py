from rest_framework.views import APIView
from .serializers import SubscriptionSerializer
from rest_framework.response import Response
from rest_framework import status
# from rest_fremework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from drf_yasg.utils import swagger_auto_schema


class CreatePaymentView(APIView):
    serializer_class = SubscriptionSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    @swagger_auto_schema(operation_summary="Api for getting payment qr code")


    def post(self,request):
        serializer = self.serializer_class(data=request.data,context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        payment_id = serializer.create_payment_custom(validated_data=request.data)
        return Response({'payment_id': payment_id}, status=status.HTTP_200_OK)
