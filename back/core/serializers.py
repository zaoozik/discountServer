from rest_framework import serializers
from .models import DiscountPlan
from orgs.models import Org, CashBox


class DiscountPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountPlan
        fields = '__all__'


class CashBoxesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashBox
        fields = '__all__'



