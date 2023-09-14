from django import forms
from .models import TradeSignals


class TradeSignalsForm(forms.ModelForm):
    class Meta:
        model = TradeSignals
        fields = '__all__'
        # ('symbol','trade_side','position_amount','leverage','trailing_stop_percent','take_profit_percent')