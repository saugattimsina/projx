from django.db import models
from ckeditor.fields import RichTextField
from user.models import User
from datetime import datetime, timedelta


# Create your models here.
class Subscription(models.Model):
    package_name = models.CharField(max_length=255)
    price = models.FloatField()
    time_in_days = models.CharField(max_length=5)
    time_in_months = models.CharField(max_length=5, null=True, blank=True)
    description = RichTextField()
    package_type = models.CharField(
        choices=(("paid", "paid"), ("free", "free")),
        max_length=255,
        blank=True,
        null=True,
    )


class SubscriptionDetail(models.Model):
    related_to = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    feature = models.CharField(max_length=255)
    is_available = models.BooleanField(default=False)


class UserSubcription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.user} - {self.plan}"

    def save(self, *args, **kwargs):
        if self.is_active:
            active_subscriptions = UserSubcription.objects.filter(
                user=self.user, is_active=True
            )
            if active_subscriptions.exists():
                active_subscriptions.update(is_active=False)
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=30)
        super().save(*args, **kwargs)


class UserSubPaymentHistory(models.Model):
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
    )
    subscription = models.ForeignKey(
        Subscription,
        null=True,
        on_delete=models.SET_NULL,
    )
    date_transaction = models.DateTimeField(
        verbose_name="transaction date",
    )
    amount = models.DecimalField(
        blank=True,
        decimal_places=4,
        max_digits=19,
        null=True,
    )
    payment_id = models.CharField(max_length=500, null=True, blank=True, unique=True)
    remaining_amount = models.DecimalField(
        blank=True, decimal_places=4, max_digits=19, null=True
    )
    payment_status = models.CharField(max_length=100, null=True, blank=True)
    has_partial_payment = models.BooleanField(default=False)


class UserWalletAddress(models.Model):
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
    )
    wallet_address = models.CharField(max_length=250)
    subscription = models.ForeignKey(
        Subscription,
        null=True,
        on_delete=models.SET_NULL,
    )
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.wallet_address}"
