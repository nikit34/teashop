# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-06-21 19:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_auto_20200621_1832'),
    ]

    operations = [
        migrations.AddField(
            model_name='productfile',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]