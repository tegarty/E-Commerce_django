# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-29 13:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='product_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
