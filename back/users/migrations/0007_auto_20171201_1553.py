# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-01 15:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_usercustom_active_to'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='usercustom',
            name='frontol_access_key_index',
        ),
        migrations.RemoveField(
            model_name='usercustom',
            name='frontol_access_key',
        ),
        migrations.RemoveField(
            model_name='usercustom',
            name='org',
        ),
        migrations.AddField(
            model_name='usercustom',
            name='licenses_number',
            field=models.IntegerField(default=0, verbose_name='Доступное количество касс'),
            preserve_default=False,
        ),
    ]
