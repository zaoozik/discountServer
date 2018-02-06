# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-27 14:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0012_auto_20171219_1546'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bonus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(default=0)),
                ('active_from', models.DateTimeField(null=True)),
                ('active_to', models.DateTimeField(null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='card',
            old_name='bonus',
            new_name='bonus_to_delete',
        ),
        migrations.AddField(
            model_name='bonus',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.Card'),
        ),
    ]