from django.db import models
from cards.models import Card
from core.models import DiscountPlan
from orgs.models import Org
from transactions.models import Transaction


# Create your models here.
class Task(models.Model):
    operation_choices = (
        ('bonus', 'Начисление бонуса'),
        ('discount', 'Пересчет скидки')
    )

    execution_date = models.DateTimeField(null=True)
    queue_date = models.DateTimeField(null=True)
    operation = models.CharField(max_length=15, null=False, choices=operation_choices)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    org = models.ForeignKey(Org, on_delete=models.CASCADE, null=True)
    data = models.FloatField(null=True)
    d_plan = models.ForeignKey(DiscountPlan, on_delete=models.CASCADE, null=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True)

    def get_operation(self):
        if self.operation=='bonus':
            return 'Начисление бонуса'
        if self.operation == 'discount':
            return 'Пересчет скидки'
