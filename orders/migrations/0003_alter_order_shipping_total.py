# Generated by Django 4.2.10 on 2024-03-16 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0002_alter_productpurchase_product"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="shipping_total",
            field=models.DecimalField(decimal_places=2, default=1.5, max_digits=100),
        ),
    ]
