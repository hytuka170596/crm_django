# Generated by Django 5.1.6 on 2025-03-07 11:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("service_product", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PromotionChannel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="The name of the promotion channel.",
                        max_length=100,
                        unique=True,
                        verbose_name="Channel Name",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="A brief description of the promotion channel.",
                        max_length=1000,
                        null=True,
                        verbose_name="Description",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AdsCompany",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "name",
                    models.CharField(
                        db_index=True, max_length=100, verbose_name="Company name"
                    ),
                ),
                (
                    "budget",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Budget"
                    ),
                ),
                (
                    "country",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("RU", "Russia"),
                            ("US", "United States"),
                            ("CN", "China"),
                            ("DE", "Germany"),
                            ("FR", "France"),
                            ("KZ", "The Republic of Kazakhstan"),
                        ],
                        max_length=100,
                        null=True,
                        verbose_name="Country",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="Email address"
                    ),
                ),
                (
                    "website",
                    models.CharField(
                        blank=True,
                        help_text="Link to the website company",
                        max_length=80,
                        null=True,
                        verbose_name="Website",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        help_text="The user who created the object.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_%(class)s",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="created by",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="service",
                        to="service_product.product",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        help_text="The user who last updated the object.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="updated_%(class)s",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="updated by",
                    ),
                ),
                (
                    "channel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="ads.promotionchannel",
                        verbose_name="Promotion channel",
                    ),
                ),
            ],
            options={
                "verbose_name": "Company",
                "verbose_name_plural": "Companies",
                "ordering": ["name", "created_at"],
                "unique_together": {("name", "website")},
            },
        ),
    ]
