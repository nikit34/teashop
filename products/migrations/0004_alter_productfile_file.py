# Generated by Django 4.2.10 on 2024-03-15 15:04

import django.core.files.storage
from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0003_alter_productfile_product"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productfile",
            name="file",
            field=models.FileField(
                blank=True,
                storage=django.core.files.storage.FileSystemStorage(
                    location="/Users/nikitapermyakov/teashop/static_cdn/protected_media"
                ),
                upload_to=products.models.upload_product_file_loc,
            ),
        ),
    ]
