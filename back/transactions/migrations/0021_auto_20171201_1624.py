# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-01 16:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0020_auto_20171201_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('Пересчет скидки', 'discount_recount'), ('Начисление бонусов', 'bonus_add'), ('Списание бонусов', 'bonus_reduce'), ('Возврат', 'refund'), ('Продажа', 'sell')], max_length=17, null=True, verbose_name='Тип'),
        ),
    ]
