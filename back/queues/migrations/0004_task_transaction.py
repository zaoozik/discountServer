# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-21 15:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0013_auto_20171121_1529'),
        ('queues', '0003_auto_20171121_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='transaction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='transactions.Transaction'),
        ),
    ]
