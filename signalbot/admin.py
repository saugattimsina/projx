from django.contrib import admin

# from .forms import TradeSignalsForm
from .models import TradeSignals, SignalFollowedBy, TradeSymbol, Portfolio, TradeHistory

# Register your models here.


admin.site.register(TradeSignals)
admin.site.register(SignalFollowedBy)
admin.site.register(TradeSymbol)
admin.site.register(Portfolio)
admin.site.register(TradeHistory)
