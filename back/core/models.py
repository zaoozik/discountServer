from django.db import models
from orgs import models as org_models
import datetime
import json


# Create your models here.
class Operations:
    bonus_reduce = 'bonus_reduce'
    bonus_add = 'bonus_add'
    sell = 'sell'
    discount_recount = 'discount_recount'
    refund = 'refund'
    bonus_refund = 'bonus_refund'


class DiscountPlan (models.Model):
    algorithm_choices = (('bonus', 'Бонусы'),
                         ('discount', 'Накопительная скидка'),
                         ('combo', 'Комбинированный')
                         )

    algorithm = models.CharField(default='bonus', max_length=100, choices=algorithm_choices, verbose_name='Режим работы')
    parameters = models.CharField(default='', null=True, max_length=400, verbose_name='Параметры бонусной системы')
    rules = models.CharField(default='', null=True, max_length=1000, verbose_name='Правила дисконтной скидки')
    org = models.OneToOneField(org_models.Org, on_delete=models.CASCADE, verbose_name='Организация')
    time_delay = models.IntegerField(default=0)

    def is_bonus(self):
        if self.algorithm == 'bonus':
            return True
        else:
            return False

    def is_discount(self):
        if self.algorithm == 'discount':
            return True
        else:
            return False

    def is_combo(self):
        if self.algorithm == 'combo':
            return True
        else:
            return False

    def get_params(self):
        if self.algorithm == 'discount':
            return None
        temp = json.loads(self.parameters)
        if type(temp) is dict:
            return temp

    def __str__(self):
        return self.org.name + '_' + self.algorithm





