from django.db import models
from cards.models import Card

# Create your models here.
class Queue(models.Model):
    operation_choices = (
        ('bonus', 'Бонус'),
        ('discount', 'Накопительная скидка')
    )

    execution_date = models.DateTimeField(null=True)
    queue_date = models.DateTimeField(null=True)
    operation = models.CharField(max_length=15, null=True, choices=operation_choices)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
