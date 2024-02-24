# Generated by Django 4.2.10 on 2024-02-24 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("addresses", "0001_initial"),
        ("billing", "0001_initial"),
        ("products", "0001_initial"),
        ("carts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductPurchase",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("order_id", models.CharField(max_length=120)),
                ("refunded", models.BooleanField(default=False)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "billing_profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="billing.billingprofile",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="products.product",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("order_id", models.CharField(blank=True, max_length=120)),
                ("address_final", models.TextField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("created", "Created"),
                            ("paid", "Paid"),
                            ("shipped", "Shipped"),
                            ("refunded", "Refunded"),
                        ],
                        default="created",
                        max_length=120,
                    ),
                ),
                (
                    "shipping_total",
                    models.DecimalField(decimal_places=2, default=5.5, max_digits=100),
                ),
                (
                    "total",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
                ),
                ("active", models.BooleanField(default=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "address",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="address",
                        to="addresses.address",
                    ),
                ),
                (
                    "billing_profile",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="billing.billingprofile",
                    ),
                ),
                (
                    "cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="carts.cart"
                    ),
                ),
            ],
            options={
                "ordering": ["-timestamp", "-updated"],
            },
        ),
    ]
