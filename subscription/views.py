from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Subscription, UserSubPaymentHistory, UserSubcription
from user.models import User
from datetime import datetime, timedelta
from rest_framework.authentication import TokenAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.
# class PaymentWebhook(APIView):
#     def post(self, request):
#         print(request.data)
#         data = request.data
#         payment_id = data["payment_id"]
#         payment_status = data["payment_status"]
#         pay_amount = int(data["pay_amount"])
#         username = data["order_id"]

#         if payment_status == "finished":
#             payment = UserSubPaymentHistory.objects.filter(
#                 payment_id=payment_id, user=User.objects.get(username=username)
#             ).first()
#             payment.payment_status = payment_status
#             # payment.save()
#             # user = payment.user
#             # user.subscription = payment.subscription
#             # user.save()
#             if int(pay_amount) - payment.amount > 0:
#                 payment.has_partial_payment = True
#                 payment.remaining_amount = pay_amount - payment.amount
#                 payment.save()
#             else:
#                 payment.has_partial_payment = False
#                 payment.remaining_amount = pay_amount - payment.amount
#                 payment.save()
#                 # user = payment.user
#                 # user.subscription = payment.subscription
#                 # user.save()
#                 # user_current_subscription = UserSubcription.objects.filter(user=payment.user,plan__package_type = 'paid').order_by('-id')
#                 # if user_current_subscription:
#                 #     user_package = user_current_subscription.first()
#                 #     # user_package.end_date = user_package.end_date + timedelta(days=int(payment.subscription.time_in_days))
#                 UserSubcription.objects.create(
#                     user=payment.user,
#                     plan=payment.subscription,
#                 )
#         return Response({"success": True})


# class SubcriptionPaymentcallback(APIView):
#     authentication_classes = [TokenAuthentication]

#     @swagger_auto_schema(
#         operation_summary="Api for payment call back",
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 "payment_id": openapi.Schema(type=openapi.TYPE_STRING),
#                 "payment_status": openapi.Schema(type=openapi.TYPE_STRING),
#                 "pay_amount": openapi.Schema(type=openapi.TYPE_INTEGER),
#                 "plan_id": openapi.Schema(type=openapi.TYPE_STRING),
#             },
#             required=["payment_id", "payment_status", "pay_amount", "plan_id"],
#         ),
#     )
#     def post(self, request, user_id):
#         payment_id = request.data["payment_id"]
#         payment_status = request.data["payment_status"]
#         pay_amount = int(request.data["pay_amount"])
#         plan_id = request.data["plan_id"]
#         if payment_status == "finished":
#             try:
#                 user = User.objects.get(id=user_id)
#                 plan = Subscription.objects.get(id=plan_id)
#                 payment = UserSubPaymentHistory.objects.filter(
#                     payment_id=payment_id, user=user
#                 ).first()
#                 print(payment)
#                 payment.payment_status = payment_status
#                 if pay_amount < plan.price:
#                     payment.has_partial_payment = True
#                     payment.remaining_amount = pay_amount - payment.amount
#                     payment.save()
#                 else:
#                     payment.has_partial_payment = False
#                     payment.remaining_amount = pay_amount - payment.amount
#                     payment.save()
#                     UserSubcription.objects.create(
#                         user=payment.user,
#                         plan=payment.subscription,
#                     )
#                     user.is_suscribed = True
#                     user.save()
#                 return Response({"success": True}, status=status.HTTP_200_OK)
#             except User.DoesNotExist:
#                 return Response(
#                     {"success": False, "message": "user not found"},
#                     status=status.HTTP_404_NOT_FOUND,
#                 )
#             except Subscription.DoesNotExist:
#                 return Response(
#                     {"success": False, "message": "plan not found"},
#                     status=status.HTTP_404_NOT_FOUND,
#                 )
