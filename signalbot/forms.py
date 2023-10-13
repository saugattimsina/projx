from django import forms
from .models import TradeSignals


# class TakeProfitForm(forms.ModelForm):
#     class Meta:
#         model = TakeProfits
#         fields = '__all__'


class TradeSignalsForm(forms.ModelForm):
    class Meta:
        model = TradeSignals
        fields = (
            "symbol",
            "price",
            "stop_amount",
            "trade_type",
            "amount_1",
            "percentage_1",
            "amount_2",
            "percentage_2",
            "amount_3",
            "percentage_3",
            "amount_4",
            "percentage_4",
        )
        # ('symbol','trade_side','position_amount','leverage','trailing_stop_percent','take_profit_percent')
