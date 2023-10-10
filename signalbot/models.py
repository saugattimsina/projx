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




class Portfolio(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    symbol = models.ForeignKey(TradeSymbol,on_delete=models.CASCADE)
    quantity = models.FloatField()
    entry_price = models.FloatField()
    stop_price = models.FloatField()
    take_profit_price = models.FloatField(blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)


class TradeHistory(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    trade_id = models.CharField(max_length=255,null=True,blank=True)
    symbol = models.CharField(max_length=255,null=True,blank=True)
    amount = models.FloatField()
    price = models.FloatField()
    trade_side = models.CharField(max_length=255,choices=(('buy','buy'),('sell','sell')))
    profit_loss = models.FloatField()
    trade_fee = models.FloatField()
    fee_currency = models.CharField(max_length=255)
    created_on = models.DateTimeField(null=True,blank=True)

 