# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-20 12:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20171120_1550'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercustom',
            name='frontol_id',
        ),
        migrations.RemoveField(
            model_name='usercustom',
            name='frontol_password',
        ),
        migrations.AddField(
            model_name='usercustom',
            name='frontol_access_key',
            field=models.CharField(max_length=128, null=True),
        ),
    ]