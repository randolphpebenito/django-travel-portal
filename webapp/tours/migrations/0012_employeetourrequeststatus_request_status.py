# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-20 05:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0011_auto_20170318_0831'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeetourrequeststatus',
            name='request_status',
            field=models.CharField(choices=[('A', 'Approve'), ('R', 'Reject'), ('RFI', 'Request For Information')], default='Pending', max_length=32),
        ),
    ]
