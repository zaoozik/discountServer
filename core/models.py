from django.db import models
from orgs import models as org_models
import datetime


# Create your models here.
class Operations:
    bonus_reduce = 'bonus_reduce'
    bonus_add = 'bonus_add'
    sell = 'sell'
    discount_recount = 'discount_recount'


class DiscountPlan (models.Model):
    algorithm_choices = (('bonus', 'Бонусы'),
                         ('discount', 'Накопительная скидка'),
                         ('combo', 'Комбинированный')
                         )

    algorithm = models.CharField(default='bonus', max_length=100, choices=algorithm_choices, verbose_name='Режим работы')
    parameters = models.CharField(default='', max_length=400, verbose_name='Параметры')
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

    def __str__(self):
        return self.org.name + '_' + self.algorithm





