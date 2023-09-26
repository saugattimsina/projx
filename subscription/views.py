from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Subscription,UserSubPaymentHistory,UserSubcription
from user.models import User
from datetime import datetime, timedelta
# Create your views here.
class PaymentWebhook(APIView):
    def post(self, request):
        print(request.data)
        data = request.data
        payment_id = data['payment_id']
        payment_status = data['payment_status']
        pay_amount = data['pay_amount']
        username = data['order_id']

        if payment_status == "finished":
            payment = UserSubPaymentHistory.objects.filter(payment_id=payment_id,user=User.objects.get(username=username)).first() 
            payment.payment_status = payment_status
            # payment.save()
            # user = payment.user
            # user.subscription = payment.subscription
            # user.save()
            if pay_amount-payment.amount>0:
                payment.has_partial_payment = True
                payment.remaining_amount = pay_amount-payment.amount
                payment.save()
            else:
                payment.has_partial_payment = False
                payment.remaining_amount = pay_amount-payment.amount
                payment.save()
                # user = payment.user
                # user.subscription = payment.subscription
                # user.save()
                UserSubcription.objects.create(
                    user = payment.user,
                    plan = payment.subscription,
                    end_date = payment.date_transaction
                )
        return Response({"success": True})
    