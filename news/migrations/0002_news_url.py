# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-01 17:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='url',
            field=models.CharField(default=0, max_length=500),
            preserve_default=False,
        ),
    ]
