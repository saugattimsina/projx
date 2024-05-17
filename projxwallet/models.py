from django.db import models
from user.models import User


# Create your models here.
class ProjxWallet(models.Model):
    amount = models.DecimalField(blank=True, decimal_places=4, max_digits=19, default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class ProjxWalletHistory(models.Model):
    class TRANSACTION_TYPE(models.TextChoices):
        DEPOSIT = (
            "deposit",
            "Deposit",
        )
        WITHDRAW = "models", "Withdraw"

    class STATUS_CHOICES(models.TextChoices):
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"
        PENDING = "pending", "Pending"

    amount = models.DecimalField(blank=True, decimal_places=4, max_digits=19, default=0)
    wallet_address = models.CharField(max_length=250, blank=True, null=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE.choices)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES.choices, default=STATUS_CHOICES.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
