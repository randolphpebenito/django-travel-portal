# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 07:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0025_auto_20170322_0744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeetourrequest',
            name='request_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emp_req_stat', to='tours.EmployeeRequestStatus'),
        ),
    ]
