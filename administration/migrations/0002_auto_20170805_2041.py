# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-05 20:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='datetime',
            field=models.DateTimeField(),
        ),
    ]