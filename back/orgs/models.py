from django.db import models
import random


# Create your models here.

class Org(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование')
    inn = models.CharField(max_length=14, default='', verbose_name='ИНН')
    kpp = models.CharField(max_length=14, default='', verbose_name='КПП')
    active_to = models.DateField(null=True)
    co_unit = None

    # def __init__(self):
    #     self.co_unit = COUnit.objects.filter(org_id__exact=self.pk)

    def __str__(self):
        return self.name

    def load_co(self):
        self.co_unit = COUnit.objects.filter(org_id__exact=self.pk)

    def is_active(self):
        if self.active_to >= datetime.now():
            return True
        else:
            return False

    # def load_cashboxes(self):
    #     self.cashboxes = CashBox.objects.filter(user_id__exact=self.pk)
    #
    # def count_cashboxes(self):
    #     self.cashboxes = CashBox.objects.filter(user_id__exact=self.pk)
    #     return len(self.cashboxes)
    #
    # def get_cashboxes(self):
    #     return CashBox.objects.filter(user_id__exact=self.pk)
    #
    # def get_cashboxes_online(self):
    #     return CashBox.objects.filter(user_id_exact=self.pk, online__exact=True)


class COUnit(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    address = models.CharField(max_length=100, verbose_name='Адрес')
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    cashboxes = None

    def load_cashboxes(self):
        self.cashboxes = CashBox.objects.filter(co_unit_id__exact=self.pk)


class CashBox(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя кассы')
    serial_number = models.CharField(max_length=20, verbose_name='Заводской номер кассы')
    frontol_key = models.CharField(max_length=64, verbose_name='Ключ Frontol', null=True)
    frontol_version = models.CharField(max_length=15, verbose_name='Версия Frontol', null=True)
    session_key = models.CharField(max_length=100, verbose_name='Сессия', null=True)
    online = models.BooleanField(verbose_name='Касса онлайн', default=False)
    online_from = models.DateTimeField(verbose_name='Дата последнего подключения', null=True)
    co_unit = models.ForeignKey(COUnit, on_delete=models.CASCADE, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['frontol_key'], name='frontol_key_index'),
        ]

    def init_frontol_key(self):
        if self.frontol_key is None:
            self.frontol_key = '%030x' % random.randrange(16 ** 64)
            try:
                self.save()
            except Exception as e:
                self.init_frontol_key()

    def set_online(self):
        self.online = True
        self.save()

    def set_offline(self):
        self.online = False
        self.save()

    def get_by_key(key):
        try:
            box = CashBox.objects.get(frontol_key__exact=key)
            return box
        except:
            return False







