from django.db import models
from orgs import models as org_models
# Create your models here.

class Card (models.Model):
    code = models.CharField(max_length=20, verbose_name='Код карты')
    accumulation = models.FloatField(default=0, verbose_name='Накопления')
    bonus = models.FloatField(default=0, verbose_name='Бонусы')
    discount = models.FloatField(default=0, verbose_name='Процентная скидка')
    holder_name = models.CharField(max_length=100, default='', verbose_name='ФИО владельца')
    org = models.ForeignKey(org_models.Org, on_delete=models.CASCADE, verbose_name='Организация')
    deleted = models.CharField(max_length=1, default='n', verbose_name='Признак удаления (y/n)')

    def __str__(self):
        return self.org.name + "_" + self.code

    class Meta:
        unique_together = (("code", "org"),)

