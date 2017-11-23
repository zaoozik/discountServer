from django.db import models
from orgs import models as org_models
# Create your models here.

class Card (models.Model):
    type_choices=(
        ('bonus', 'Бонусная'),
        ('discount', 'Дисконтная'),
        ('combo', 'Комбинированная')
    )

    code = models.CharField(max_length=20, verbose_name='Код карты')
    accumulation = models.FloatField(default=0, verbose_name='Накопления')
    bonus = models.FloatField(default=0, verbose_name='Бонусы')
    discount = models.FloatField(default=0, verbose_name='Процентная скидка')
    holder_name = models.CharField(max_length=100, default='', verbose_name='ФИО владельца')
    org = models.ForeignKey(org_models.Org, on_delete=models.CASCADE, verbose_name='Организация')
    deleted = models.CharField(max_length=1, default='n', verbose_name='Признак удаления (y/n)')
    type = models.CharField(max_length=17, default='bonus', choices=type_choices, verbose_name='Тип карты')
    reg_date = models.DateField(null=True, verbose_name='Дата регистрации')
    changes_date = models.DateField(null=True, verbose_name='Дата последних изменений')
    last_transaction_date = models.DateField(null=True, verbose_name='Дата последней транзакции')

    def is_bonus(self):
        if self.type == 'bonus':
            return True
        else:
            return False

    def is_discount(self):
        if self.type == 'discount':
            return True
        else:
            return False

    def is_combo(self):
        if self.type == 'combo':
            return True
        else:
            return False

    def get_type(self):
        if self.type == 'bonus':
            return 'Бонусная'
        if self.type == 'discount':
            return 'Дисконтная'
        if self.type == 'combo':
            return 'Комбинированная'

    def __str__(self):
        return self.org.name + "_" + self.code

    class Meta:
        unique_together = (("code", "org"),)

