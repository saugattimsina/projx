from django.db import models
from user.models import User
# Create your models here.


class TradeSymbol(models.Model):
    symbol = models.CharField(max_length=255)
    base_asset = models.CharField(max_length=255)
    quote_asset = models.CharField(max_length=255)
    # symbol_name = models.CharField(max_length=255)
    def __str__(self):
        return self.symbol
    
class TradeSignals(models.Model):
    symbol = models.ForeignKey(TradeSymbol,on_delete=models.CASCADE)
    # trade_side = models.CharField(max_length=255)
    price = models.FloatField()
    # leverage = models.FloatField()
    stop_amount = models.FloatField() 
    take_profit_amount = models.FloatField()   
    created_on = models.DateTimeField(auto_now_add=True)


class SignalFollowedBy(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    signal = models.ForeignKey(TradeSignals,on_delete=models.CASCADE)
    is_cancelled = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)





