# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-26 10:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
