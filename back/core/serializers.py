from rest_framework import serializers
from .models import DiscountPlan


class DiscountPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountPlan
        fields = '__all__'



