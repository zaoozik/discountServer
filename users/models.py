from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from orgs.models import Org
import random


class UserCustom(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    cashboxes = None
    active_to = models.DateField(null=True)
    licenses_count = models.IntegerField(verbose_name='Доступное количество касс')

    def is_active(self):
        if self.active_to >= datetime.now():
            return True
        else:
            return False

    def load_cashboxes(self):
        self.cashboxes = CashBox.objects.filter(user_id__exact=self.pk)

    def count_cashboxes(self):
        self.cashboxes = CashBox.objects.filter(user_id__exact=self.pk)
        return len(self.cashboxes)

    def get_cashboxes(self):
        return CashBox.objects.filter(user_id__exact=self.pk)

    def get_cashboxes_online(self):
        return CashBox.objects.filter(user_id_exact=self.pk, online__exact=True)


class CashBox(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя кассы')
    serial_number = models.CharField(max_length=20, verbose_name='Заводской номер кассы')
    address = models.CharField(max_length=100, verbose_name='Адрес кассы')
    user = models.ForeignKey(UserCustom, on_delete=models.CASCADE)
    frontol_key = models.CharField(max_length=64, verbose_name='Ключ Frontol', null=True)
    session_key = models.CharField(max_length=100, verbose_name='Сессия', null=True)
    online = models.BooleanField(verbose_name='Касса онлайн', default=False)

    class Meta:
        indexes = [
            models.Index(fields=['frontol_key'], name='frontol_index'),
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

