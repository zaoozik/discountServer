# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-21 06:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cards', '0009_auto_20171115_1013'),
    ]

    operations = [
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('execution_date', models.DateTimeField(null=True)),
                ('queue_date', models.DateTimeField(null=True)),
                ('operation', models.CharField(choices=[('bonus', 'Бонус'), ('discount', 'Накопительная скидка')], max_length=15, null=True)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.Card')),
            ],
        ),
    ]