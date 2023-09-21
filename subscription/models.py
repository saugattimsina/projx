from django.db import models
from ckeditor.fields import RichTextField
from user.models import User


# Create your models here.
class Subscription(models.Model):
    package_name = models.CharField(max_length=255)
    price = models.FloatField()
    time_in_days = models.CharField(max_length=5)
    description = RichTextField()
    package_type= models.CharField(choices=(("paid",'paid'),("free","free")),max_length=255,blank=True,null=True)


class SubscriptionDetail(models.Model):
    related_to = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    feature = models.CharField(max_length=255)
    is_available = models.BooleanField(default=False)


class UserSubcription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.user} - {self.plan}"


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
    payment_status = models.CharField(max_length=100, null=True, blank=True)
