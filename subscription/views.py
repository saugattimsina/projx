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
        pay_amount = int(data['pay_amount'])
        username = data['order_id']

        if payment_status == "finished":
            payment = UserSubPaymentHistory.objects.filter(payment_id=payment_id,user=User.objects.get(username=username)).first() 
            payment.payment_status = payment_status
            # payment.save()
            # user = payment.user
            # user.subscription = payment.subscription
            # user.save()
            if int(pay_amount)-payment.amount>0:
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
                # user_current_subscription = UserSubcription.objects.filter(user=payment.user,plan__package_type = 'paid').order_by('-id')
                # if user_current_subscription:
                #     user_package = user_current_subscription.first()
                #     # user_package.end_date = user_package.end_date + timedelta(days=int(payment.subscription.time_in_days))
                UserSubcription.objects.create(
                    user = payment.user,
                    plan = payment.subscription,
                )
        return Response({"success": True})
    