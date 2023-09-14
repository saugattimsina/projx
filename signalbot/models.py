from django.db import models

# Create your models here.
class TradeSignals(models.Model):
    symbol = models.CharField(max_length=255)
    trade_side = models.CharField(max_length=255)
    position_amount = models.FloatField()
    leverage = models.FloatField()
    trailing_stop_percent = models.FloatField() 
    take_profit_percent = models.FloatField()   