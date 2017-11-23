# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-21 14:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0011_auto_20171121_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('Начисление бонусов', 'bonus_add'), ('Пересчет скидки', 'discount_recount'), ('Списание бонусов', 'bonus_reduce'), ('Продажа', 'sell')], max_length=17, null=True, verbose_name='Тип'),
        ),
    ]