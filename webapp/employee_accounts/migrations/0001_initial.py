# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-16 15:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(blank=True, max_length=64)),
                ('lastname', models.CharField(blank=True, max_length=64)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Account',
            },
        ),
        migrations.CreateModel(
            name='EmployeeAccountPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_name', models.CharField(blank=True, max_length=64)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Position',
            },
        ),
        migrations.AddField(
            model_name='employeeaccount',
            name='account_position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='position', to='employee_accounts.EmployeeAccountPosition'),
        ),
    ]
