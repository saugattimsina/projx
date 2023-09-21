from django.contrib import admin

from .models import Subscription, SubscriptionDetail, UserSubcription, UserSubPaymentHistory

# Register your models here.
admin.site.register(Subscription)
admin.site.register(SubscriptionDetail)
admin.site.register(UserSubcription)
admin.site.register(UserSubPaymentHistory)