# Generated by Django 5.1.6 on 2025-03-09 18:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ads", "0001_initial"),
        ("leads", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lead",
            name="campaign",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="leads",
                to="ads.adscompany",
                verbose_name="Campaign",
            ),
        ),
    ]
