from rest_framework.views import APIView
from .serializers import SubscriptionSerializer
from rest_framework.response import Response
from rest_framework import status
# from rest_fremework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


def CreatePaymentView(APIView):
    serializer_class = SubscriptionSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment_id = serializer.create_payment_custom(validated_data=request.data,context={'user':request.user})
        return Response({'payment_id': payment_id}, status=status.HTTP_200_OK)
