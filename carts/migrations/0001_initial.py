# Generated by Django 4.2.10 on 2024-02-24 19:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("products", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Cart",
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
                (
                    "subtotal",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
                ),
                (
                    "total",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
                ),
                ("updated", models.DateTimeField(auto_now=True)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("products", models.ManyToManyField(blank=True, to="products.product")),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
