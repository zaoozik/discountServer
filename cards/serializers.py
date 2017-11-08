from rest_framework import serializers
from cards.models import Card


class CardSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(required=False, allow_blank=True, max_length=100)
    accumulation = serializers.FloatField(required=False)
    #org = serializers.Ch

