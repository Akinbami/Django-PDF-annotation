# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-02 05:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20180218_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='is_reverted',
            field=models.BooleanField(default=False),
        ),
    ]
