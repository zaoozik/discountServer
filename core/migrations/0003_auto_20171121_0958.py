# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-21 06:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20171115_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discountplan',
            name='algorithm',
            field=models.CharField(choices=[('bonus', 'Бонусы'), ('discount', 'Накопительная скидка'), ('combo', 'Комбинированный')], default='bonus', max_length=100, verbose_name='Режим работы'),
        ),
    ]
