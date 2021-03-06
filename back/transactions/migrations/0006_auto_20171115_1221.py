# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 09:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_auto_20171115_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='doc_close_user',
            field=models.CharField(max_length=100, null=True, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='doc_external_id',
            field=models.CharField(max_length=20, null=True, verbose_name='Внешний номер документа'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='doc_number',
            field=models.CharField(max_length=20, null=True, verbose_name='Номер документа'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='session',
            field=models.CharField(max_length=20, null=True, verbose_name='Номер смены'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='workplace',
            field=models.CharField(max_length=20, null=True, verbose_name='Код рабочего места'),
        ),
    ]
