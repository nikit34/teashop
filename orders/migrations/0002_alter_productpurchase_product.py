# Generated by Django 4.2.10 on 2024-03-15 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0004_alter_productfile_file"),
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productpurchase",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="products.product"
            ),
        ),
    ]
