# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 07:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_transaction_bonus_add'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='bonus_before',
            field=models.FloatField(default=0, verbose_name='Бонусов до операции'),
        ),
    ]
