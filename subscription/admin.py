from django.contrib import admin

from .models import (
    Subscription,
    SubscriptionDetail,
    UserSubcription,
    UserSubPaymentHistory,
)

# Register your models here.
admin.site.register(Subscription)
admin.site.register(SubscriptionDetail)
admin.site.register(UserSubPaymentHistory)


@admin.register(UserSubcription)
class UserSubcriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "start_date", "end_date", "created_on")
    list_filter = ["plan", "start_date", "end_date"]
