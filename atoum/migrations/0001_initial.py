# Generated by Django 5.0.9 on 2024-09-23 14:59

import django.db.models.deletion
import django.utils.timezone
import smart_media.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Assortment",
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
                    "created",
                    models.DateTimeField(
                        db_index=True,
                        default=django.utils.timezone.now,
                        verbose_name="creation date",
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        db_index=True,
                        default=django.utils.timezone.now,
                        verbose_name="modification date",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        default="", max_length=100, unique=True, verbose_name="title"
                    ),
                ),
                (
                    "slug",
                    models.CharField(
                        default="", max_length=130, unique=True, verbose_name="slug"
                    ),
                ),
            ],
            options={
                "verbose_name": "Assortment",
                "verbose_name_plural": "Assortments",
                "ordering": ["title"],
            },
        ),
        migrations.CreateModel(
            name="Blog",
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
                    "title",
                    models.CharField(
                        default="", max_length=55, unique=True, verbose_name="title"
                    ),
                ),
            ],
            options={
                "verbose_name": "Blog",
                "verbose_name_plural": "Blogs",
                "ordering": ["title"],
            },
        ),
        migrations.CreateModel(
            name="Brand",
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
                    "created",
                    models.DateTimeField(
                        db_index=True,
                        default=django.utils.timezone.now,
                        verbose_name="creation date",
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        db_index=True,
                        default=django.utils.timezone.now,
                        verbose_name="modification date",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        default="", max_length=100, unique=True, verbose_name="title"
                    ),
                ),
                (
                    "slug",
                    models.CharField(
                        default="", max_length=130, unique=True, verbose_name="slug"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, default="", verbose_name="description"
                    ),
                ),
                (
                    "cover",
                    smart_media.modelfields.SmartMediaField(
                        blank=True,
                        default="",
                        max_length=255,
                        upload_to="atoum/brand/cover/%y/%m",
                        verbose_name="cover image",
                    ),
                ),
            ],
            options={
                "verbose_name": "Brand",
                "verbose_name_plural": "Brands",
                "ordering": ["title"],
            },
        ),
        migrations.CreateModel(
            name="Consumable",
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
                    "created",
                    models.DateTimeField(
                        db_index=True,
                        default=django.utils.timezone.now,
                        verbose_name="creation date",
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        db_index=True,
                        default=django.utils.timezone.now,
                        verbose_name="modification date",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        default="", max_length=100, unique=True, verbose_name="title"
                    ),
                ),
                (
                    "slug",
                    models.CharField(
                        default="", max_length=130, unique=True, verbose_name="slug"
                    ),
                ),
            ],
            options={
                "verbose_name": "Consumable",
                "verbose_name_plural": "Consumables",
                "ordering": ["title"],
            },
        ),
        migrations.CreateModel(
            name="Article",
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
                    "title",
                    models.CharField(default="", max_length=150, verbose_name="title"),
                ),
                (
                    "content",
                    models.TextField(blank=True, default="", verbose_name="content"),
                ),
                (
                    "publish_start",
                    models.DateTimeField(
                        db_index=True,
                        default=django.utils.timezone.now,
                        verbose_name="publication start",
                    ),
                ),
                (
                    "blog",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="atoum.blog",
                        verbose_name="Related blog",
                    ),
                ),
            ],
            options={
                "verbose_name": "Article",
                "verbose_name_plural": "Articles",
                "ordering": ["-publish_start"],
            },
        ),
        migrations.CreateModel(
            name="Category",
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
                    "created",
                    models.DateTimeField(
                        db_index=True,
                        default=django.utils.timezone.now,
                        verbose_name="creation date",
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        db_index=True,
                        default=django.utils.timezone.now,
                        verbose_name="modification date",
                    ),
                ),
                (
                    "title",
                    models.CharField(default="", max_length=100, verbose_name="title"),
                ),
                (
                    "slug",
                    models.CharField(default="", max_length=130, verbose_name="slug"),
                ),
                (
                    "assortment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="atoum.assortment",
                        verbose_name="Assortment",
                    ),
                ),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
                "ordering": ["title"],
            },
        ),
        migrations.AddField(
            model_name="assortment",
            name="consumable",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="atoum.consumable",
                verbose_name="Consumable",
            ),
        ),
        migrations.CreateModel(
            name="Product",
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
                    "created",
                    models.DateTimeField(
                        db_index=True,
                        default=django.utils.timezone.now,
                        verbose_name="creation date",
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        db_index=True,
                        default=django.utils.timezone.now,
                        verbose_name="modification date",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        default="", max_length=100, unique=True, verbose_name="title"
                    ),
                ),
                (
                    "slug",
                    models.CharField(
                        default="", max_length=130, unique=True, verbose_name="slug"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, default="", verbose_name="description"
                    ),
                ),
                (
                    "cover",
                    smart_media.modelfields.SmartMediaField(
                        blank=True,
                        default="",
                        max_length=255,
                        upload_to="atoum/product/cover/%y/%m",
                        verbose_name="cover image",
                    ),
                ),
                (
                    "brand",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="atoum.brand",
                        verbose_name="brand",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="atoum.category",
                        verbose_name="Category",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product",
                "verbose_name_plural": "Products",
                "ordering": ["title"],
            },
        ),
        migrations.AddConstraint(
            model_name="category",
            constraint=models.UniqueConstraint(
                fields=("assortment", "title"), name="atoum_unique_cat_assortment_title"
            ),
        ),
        migrations.AddConstraint(
            model_name="category",
            constraint=models.UniqueConstraint(
                fields=("assortment", "slug"), name="atoum_unique_cat_assortment_slug"
            ),
        ),
    ]
