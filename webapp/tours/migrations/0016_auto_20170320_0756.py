# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-20 07:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0015_auto_20170320_0754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeetourrequest',
            name='request_status',
            field=models.CharField(default='Pending', max_length=32),
        ),
        migrations.DeleteModel(
            name='EmployeeRequestStatus',
        ),
    ]