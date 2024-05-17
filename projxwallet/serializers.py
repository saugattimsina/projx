from rest_framework import serializers

from .models import ProjxWallet, ProjxWalletHistory


class ProjxWalletHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjxWalletHistory
        fields = "__all__"


class ProjxWalletSerializer(serializers.Serializer):
    wallet_address = serializers.CharField(max_length=250)
    amount = serializers.DecimalField(decimal_places=4, max_digits=19)
