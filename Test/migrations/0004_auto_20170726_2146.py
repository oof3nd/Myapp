# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-26 16:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0003_auto_20170726_2143'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='user',
            new_name='owner',
        ),
    ]
