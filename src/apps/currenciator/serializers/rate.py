from rest_framework import serializers

from src.apps.currenciator.models import Rate


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ('rate', 'avg_volume')
