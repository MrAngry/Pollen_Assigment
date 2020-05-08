from rest_framework import serializers

from rewards.models import RecommendedReward


class RecommendedRewardSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecommendedReward
        fields = '__all__'
