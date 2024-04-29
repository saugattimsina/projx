from binarytree.models import MLMRank

from rest_framework import serializers


class MLMRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLMRank
        fields = [
            "id",
            "rank_image",
            "rank_name",
            "direct_referrals",
            "active_members",
            "separate_enroller_tree_conditions",
        ]
