# Generated by Django 4.2.10 on 2024-04-07 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0005_order_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="description",
            field=models.TextField(blank=True, max_length=30, null=True),
        ),
    ]