# Generated by Django 4.2.10 on 2024-03-31 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("addresses", "0005_alter_address_billing_profile"),
        ("orders", "0003_alter_order_shipping_total"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="address",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="address",
                to="addresses.address",
            ),
        ),
    ]
