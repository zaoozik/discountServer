# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-04 15:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0008_auto_20171201_1608'),
        ('users', '0011_auto_20171211_1011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cashbox',
            name='user',
        ),
        migrations.AddField(
            model_name='cashbox',
            name='org',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orgs.Org'),
        ),
    ]