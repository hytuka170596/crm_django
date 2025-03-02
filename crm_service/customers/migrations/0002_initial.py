# Generated by Django 5.1.6 on 2025-03-02 14:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("customers", "0001_initial"),
        ("leads", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="lead",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="customer",
                to="leads.lead",
                verbose_name="Lead",
            ),
        ),
        migrations.AddField(
            model_name="customer",
            name="updated_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="updated_%(class)s",
                to=settings.AUTH_USER_MODEL,
                verbose_name="updated by",
            ),
        ),
        migrations.AddIndex(
            model_name="customer",
            index=models.Index(
                fields=["created_at"], name="customers_c_created_1ed0f4_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="customer",
            index=models.Index(
                fields=["updated_at"], name="customers_c_updated_7518c4_idx"
            ),
        ),
    ]
