from django.db import models
from users.models import UserCustom
import random

# Create your models here.
class Org (models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование')
    active_from = models.DateTimeField(null=True)
    active_to = models.DateTimeField(null=True)
    inn = models.CharField(max_length=14, default='', verbose_name='ИНН')
    kpp = models.CharField(max_length=14, default='', verbose_name='КПП')

    def __str__(self):
        return self.name


class CashBox(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя кассы')
    serial_number = models.CharField(max_length=20, verbose_name='Заводской номер кассы')
    address = models.CharField(max_length='100', verbose_name='Адрес кассы')
    user = models.ForeignKey(UserCustom, on_delete=models.CASCADE)
    frontol_key = models.CharField(max_length=64, verbose_name='Ключ Frontol', null=True)

    class Meta:
        indexes = [
            models.Index(fields=['frontol_key'], name='frontol_index'),
        ]

    def init_frontol_key(self):
        if self.frontol_key is None:
            self.frontol_key = '%030x' % random.randrange(16 ** 64)


