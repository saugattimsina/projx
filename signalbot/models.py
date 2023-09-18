from django.db import models
from user.models import User
# Create your models here.
class TradeSignals(models.Model):
    symbol = models.CharField(max_length=255)
    # trade_side = models.CharField(max_length=255)
    price = models.FloatField()
    # leverage = models.FloatField()
    stop_amount = models.FloatField() 
    take_profit_amount = models.FloatField()   
    created_on = models.DateTimeField(auto_now_add=True)


class SignalFollowedBy(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    signal = models.ForeignKey(TradeSignals,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)


