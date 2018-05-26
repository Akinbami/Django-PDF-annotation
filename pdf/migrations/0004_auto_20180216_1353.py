# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-16 13:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf', '0003_pdf_contributors'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pdf',
            old_name='contributors',
            new_name='contributor',
        ),
        migrations.AddField(
            model_name='pdf',
            name='comment',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]