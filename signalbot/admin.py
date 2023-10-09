from django.contrib import admin
# from .forms import TradeSignalsForm
from .models import TradeSignals,SignalFollowedBy,TradeSymbol
# Register your models here.


admin.site.register(TradeSignals)
admin.site.register(SignalFollowedBy)
admin.site.register(TradeSymbol)