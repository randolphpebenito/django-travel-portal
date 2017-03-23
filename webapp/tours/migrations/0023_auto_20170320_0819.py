# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-20 08:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0022_auto_20170320_0814'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employeerequeststatus',
            options={'verbose_name_plural': 'Employee Request Status'},
        ),
        migrations.AlterModelOptions(
            name='employeetourrequeststatus',
            options={'verbose_name_plural': 'Employee Tour Request Status'},
        ),
        migrations.AlterField(
            model_name='employeetourrequest',
            name='request_status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='emp_req_stat', to='tours.EmployeeRequestStatus'),
        ),
        migrations.AlterField(
            model_name='employeetourrequeststatus',
            name='approved_by_finance_manager',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='finance_manager_status', to='tours.EmployeeRequestStatus'),
        ),
        migrations.AlterField(
            model_name='employeetourrequeststatus',
            name='approved_by_manager',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='manager_status', to='tours.EmployeeRequestStatus'),
        ),
    ]
