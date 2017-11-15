# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 07:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discountplan',
            name='algorithm',
            field=models.CharField(choices=[('bonus', 'Бонусы'), ('discount', 'Накопительная скидка')], default='bonus', max_length=100, verbose_name='Режим работы'),
        ),
        migrations.AlterField(
            model_name='discountplan',
            name='org',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='orgs.Org', verbose_name='Организация'),
        ),
        migrations.AlterField(
            model_name='discountplan',
            name='parameters',
            field=models.CharField(default='', max_length=400, verbose_name='Параметры'),
        ),
    ]