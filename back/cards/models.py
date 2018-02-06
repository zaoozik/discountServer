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
    bonus_to_delete = models.FloatField(default=0, verbose_name='Бонусы')
    discount = models.FloatField(default=0, verbose_name='Процентная скидка')
    holder_name = models.CharField(max_length=100, default='', verbose_name='ФИО владельца')
    holder_phone = models.CharField(max_length=20, null=True, default='+7', verbose_name='Телефон')
    sex = models.CharField(max_length=1, default='m', verbose_name='Пол')
    fav_date = models.DateField(verbose_name='Знаменательная дата', null=True)
    org = models.ForeignKey(org_models.Org, on_delete=models.CASCADE, verbose_name='Организация')
    deleted = models.CharField(max_length=1, default='n', verbose_name='Признак удаления (y/n)')
    type = models.CharField(max_length=17, default='bonus', choices=type_choices, verbose_name='Тип карты')
    reg_date = models.DateField(null=True, verbose_name='Дата регистрации')
    changes_date = models.DateField(null=True, verbose_name='Дата последних изменений')
    last_transaction_date = models.DateField(null=True, verbose_name='Дата последней транзакции')

    class Meta:
        indexes = [
            models.Index(fields=['code'], name = 'code_index'),
        ]

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

    def get_total_bonus(self):
        bonuses = Bonus.objects.filter(card_id__exact=self.pk)
        result = 0
        for bonus in bonuses:
            result += bonus.value
        return result

    def get_bonuses(self):
        return Bonus.objects.filter(card_id__exact=self.pk)

    def get_bonuses_array(self):
        bonuses = []
        bonus_dict = {}
        for bonus in Bonus.objects.filter(card_id__exact=self.pk):
            bonus_dict = {}
            bonus_dict['id'] = bonus.pk
            bonus_dict['value'] = bonus.value
            bonus_dict['active_from'] = bonus.active_from
            bonus_dict['active_to'] = bonus.active_to
            bonuses.append(bonus_dict)
        return bonuses

    def __str__(self):
        return self.org.name + "_" + self.code

    class Meta:
        unique_together = (("code", "org"),)


class Bonus (models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    value = models.FloatField(default=0)
    active_from = models.DateTimeField(null=True)
    active_to = models.DateTimeField(null=True)
    #transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)































