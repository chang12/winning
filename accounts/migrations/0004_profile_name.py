# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-24 08:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
