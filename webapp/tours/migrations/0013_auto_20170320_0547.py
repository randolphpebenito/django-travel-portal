# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-20 05:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0012_employeetourrequeststatus_request_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeetourrequeststatus',
            name='finance_manager_req_for_info',
        ),
        migrations.RemoveField(
            model_name='employeetourrequeststatus',
            name='manager_req_for_info',
        ),
        migrations.RemoveField(
            model_name='employeetourrequeststatus',
            name='request_status',
        ),
        migrations.AlterField(
            model_name='employeetourrequeststatus',
            name='approved_by_finance_manager',
            field=models.CharField(choices=[('P', 'Pending'), ('A', 'Approve'), ('R', 'Reject'), ('RFI', 'Request For Information')], default='Pending', max_length=32),
        ),
        migrations.AlterField(
            model_name='employeetourrequeststatus',
            name='approved_by_manager',
            field=models.CharField(choices=[('P', 'Pending'), ('A', 'Approve'), ('R', 'Reject'), ('RFI', 'Request For Information')], default='Pending', max_length=32),
        ),
        migrations.AlterField(
            model_name='employeetourrequeststatus',
            name='approving_finance_manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='finance_manager', to='employee_accounts.EmployeeAccount'),
        ),
    ]
