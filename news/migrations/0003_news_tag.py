# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-01 17:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_news_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='tag',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
    ]
