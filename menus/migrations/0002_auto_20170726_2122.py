# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-26 16:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='contents',
            field=models.TextField(help_text='Через запятую'),
        ),
        migrations.AlterField(
            model_name='item',
            name='excludes',
            field=models.TextField(blank=True, help_text='Через запятую', null=True),
        ),
    ]
