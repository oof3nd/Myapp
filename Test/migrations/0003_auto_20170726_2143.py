# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-26 16:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0002_auto_20170715_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Заголовок'),
        ),
    ]
