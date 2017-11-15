from django.db import models

# Create your models here.
class Org (models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование')
    active_from = models.DateTimeField(null=True)
    active_to = models.DateTimeField(null=True)
    inn = models.CharField(max_length=14, default='', verbose_name='ИНН')
    kpp = models.CharField(max_length=14, default='', verbose_name='КПП')

    def __str__(self):
        return self.name
