# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-17 15:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0004_employeetourrequeststatus_approving_finance_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeetourrequest',
            name='draft',
            field=models.BooleanField(default=False),
        ),
    ]