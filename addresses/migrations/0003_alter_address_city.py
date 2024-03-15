# Generated by Django 4.2.10 on 2024-03-12 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("addresses", "0002_alter_address_city_alter_address_country_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="address",
            name="city",
            field=models.CharField(
                choices=[
                    ("Porto", "Porto"),
                    ("Vila Nova de Gaia", "Vila Nova de Gaia"),
                ],
                max_length=120,
            ),
        ),
    ]
