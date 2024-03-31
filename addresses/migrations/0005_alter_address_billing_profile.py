# Generated by Django 4.2.10 on 2024-03-31 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("billing", "0005_remove_charge_outcome_remove_charge_outcome_type_and_more"),
        ("addresses", "0004_alter_address_billing_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="address",
            name="billing_profile",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="billing.billingprofile",
            ),
        ),
    ]