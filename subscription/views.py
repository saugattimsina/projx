from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# fr

# Create your views here.
class PaymentWebhook(APIView):
    def post(self, request):
        print(request.data)

        return Response({"success": True})
    