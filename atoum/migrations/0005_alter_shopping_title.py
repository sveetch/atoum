# Generated by Django 5.0.9 on 2025-01-08 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("atoum", "0004_shopping_done"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shopping",
            name="title",
            field=models.CharField(
                blank=True, default="", max_length=100, verbose_name="title"
            ),
        ),
    ]