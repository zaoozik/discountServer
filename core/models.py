from django.db import models
from orgs import models as org_models
import datetime


# Create your models here.
class DiscountPlan (models.Model):
    algorithm_choices = (('bonus', 'Бонусы'),
                         ('discount', 'Накопительная скидка'))

    algorithm = models.CharField(default='bonus', max_length=100, choices=algorithm_choices, verbose_name='Режим работы')
    parameters = models.CharField(default='', max_length=400, verbose_name='Параметры')
    org = models.OneToOneField(org_models.Org, on_delete=models.CASCADE, verbose_name='Организация')

    def __str__(self):
        return self.org.name + '_' + self.algorithm




