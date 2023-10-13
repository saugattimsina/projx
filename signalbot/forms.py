from django import forms
from .models import TradeSignals,TakeProfits



class TakeProfitForm(forms.ModelForm):
    class Meta:
        model = TakeProfits
        fields = '__all__'

class TradeSignalsForm(forms.ModelForm):
    class Meta:
        model = TradeSignals
        fields = ('symbol','price','stop_amount','trade_type')
        # ('symbol','trade_side','position_amount','leverage','trailing_stop_percent','take_profit_percent')