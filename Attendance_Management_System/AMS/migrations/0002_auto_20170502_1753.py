# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-02 09:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AMS', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salary',
            name='gonghao',
            field=models.CharField(max_length=200),
        ),
    ]