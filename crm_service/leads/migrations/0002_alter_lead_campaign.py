# Generated by Django 5.1.6 on 2025-03-02 18:45

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
                to="ads.adscompany",
                verbose_name="Campaign",
            ),
        ),
    ]
