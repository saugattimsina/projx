from django.db import models

# Create your models here.
class TradeSignals(models.Model):
    symbol = models.CharField(max_length=255)
    # trade_side = models.CharField(max_length=255)
    price = models.FloatField()
    # leverage = models.FloatField()
    stop_amount = models.FloatField() 
    take_profit_amount = models.FloatField()   