# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-06-22 12:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_productfile_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='is_delivery',
            new_name='delivery',
        ),
    ]