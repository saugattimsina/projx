from django.contrib import admin

# from .forms import TradeSignalsForm
from .models import (
    TradeSignals,
    SignalFollowedBy,
    TradeSymbol,
    Portfolio,
    TradeHistory,
    ReferalIncome,
    ReferalWallet,
    BinaryIncome,
    Binawallet,
)

# Register your models here.


admin.site.register(TradeSignals)
admin.site.register(SignalFollowedBy)
admin.site.register(TradeSymbol)
admin.site.register(Portfolio)
admin.site.register(ReferalIncome)
admin.site.register(ReferalWallet)
admin.site.register(Binawallet)
admin.site.register(BinaryIncome)


@admin.register(TradeHistory)
class TradeHistoryAdmin(admin.ModelAdmin):
    list_display = ["user", "trade_id", "amount", "price", "profit_loss"]
