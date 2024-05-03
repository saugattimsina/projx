from django.db import models
from user.models import User

# from signalbot.models import TradeSymbol


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.ForeignKey(
        "signalbot.TradeSymbol", on_delete=models.SET_NULL, null=True
    )
    trade_direction = models.CharField(max_length=50, null=True, blank=True)
    order_id = models.CharField(max_length=100, unique=True)
    entry_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    avg_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    filled_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remaining_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    related_order = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )
    filled = models.BooleanField(default=False)
    executed_date_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserActivePositions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.ForeignKey(
        "signalbot.TradeSymbol", on_delete=models.SET_NULL, null=True
    )
    entry_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mark_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    liquidationPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    breakEvenPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    marginRatio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    margin = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    margin_percentage = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pnl = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pnl_percentage = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
