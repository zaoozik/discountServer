# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-08 11:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0001_initial'),
        ('cards', '0003_card_accumulation'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='card',
            unique_together=set([('code', 'org')]),
        ),
    ]