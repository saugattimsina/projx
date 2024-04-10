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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get("price")
        stop_amount = cleaned_data.get("stop_amount")
        amount_1 = cleaned_data.get("amount_1")
        amount_2 = cleaned_data.get("amount_2")
        amount_3 = cleaned_data.get("amount_3")
        amount_4 = cleaned_data.get("amount_4")
        percentage_1 = cleaned_data.get("percentage_1")
        percentage_2 = cleaned_data.get("percentage_2")
        percentage_3 = cleaned_data.get("percentage_3")
        percentage_4 = cleaned_data.get("percentage_4")

        if stop_amount and price and stop_amount >= price:
            self.add_error("stop_amount", "Stop amount should be less than price.")

        if price and (amount_1 + amount_2 + amount_3 + amount_4) <= price:
            self.add_error("amount_1", "Sum of 4 amounts should be greater than price.")

        total_percentage = percentage_1 + percentage_2 + percentage_3 + percentage_4
        if total_percentage != 100:
            self.add_error("percentage_1", "Total percentage should be 100.")
