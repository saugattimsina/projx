from .models import UserActivePositions

from rest_framework import serializers


class UserActivePositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivePositions
        fields = "__all__"
