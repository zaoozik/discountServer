from django.db import models
from orgs.models import Org
from cards.models import Card
from core.models import Operations


# Create your models here.
class Transaction(models.Model):
    type_choices = {
        ('Списание бонусов', 'bonus_reduce'),
        ('Начисление бонусов', 'bonus_add'),
        ('Продажа', 'sell'),
        ('Пересчет скидки', 'discount_recount'),
        ('Возврат', 'refund'),

    }
    type = models.CharField(verbose_name='Тип',max_length=17, null=True, choices=type_choices)
    date = models.DateTimeField(verbose_name='Дата/Время', null=True)
    org = models.ForeignKey(Org, on_delete=models.CASCADE, verbose_name='Организация')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, verbose_name='Карта')
    sum = models.FloatField(default=0, verbose_name='Сумма пришедшая')
    bonus_before = models.FloatField(null=True, verbose_name='Бонусов до операции')
    bonus_add = models.FloatField(default=0, verbose_name='Начисление бонусов')
    bonus_reduce = models.FloatField(default=0, verbose_name='Списание бонусов')
    workplace = models.CharField(verbose_name='Код рабочего места', null=True, max_length=20)
    doc_number = models.CharField(verbose_name='Номер документа', null=True, max_length=20)
    session = models.CharField(verbose_name='Номер смены', null=True, max_length=20)
    doc_external_id = models.CharField(verbose_name='Внешний номер документа', null=True, max_length=20)
    doc_close_user = models.CharField(verbose_name='Пользователь', max_length=100, null=True)
    shop = models.IntegerField(verbose_name='Номер мазагина', null=True)

    def create(self, values):
        if 'workplace' in values:
            self.workplace = values['workplace']
        if 'doc_number' in values:
            self.doc_number = values['doc_number']
        if 'session' in values:
            self.session = values['session']
        if 'doc_external_id' in values:
            self.doc_external_id = values['doc_external_id']
        if 'doc_close_user' in values:
            self.doc_close_user = values['doc_close_user']
        if 'shop' in values:
            self.shop = values['shop']
        return self

    def return_type(self):
        if self.type == Operations.sell:
            return "<span style='color: blue;'>Продажа</span>"
        elif self.type == Operations.bonus_reduce:
            return "<span style='color: red;'>Списание бонусов</span>"
        elif self.type == Operations.refund:
            return "<span style='color: red;'>Возврат</span>"
        elif self.type == Operations.bonus_add:
            return "<span style='color: green;'>Начисление бонусов</span>"
        elif self.type == Operations.discount_recount:
            return "<span style='color: orange;'>Пересчет скидки</span>"
