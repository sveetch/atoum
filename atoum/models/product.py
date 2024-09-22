from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone

from smart_media.mixins import SmartFormatMixin
from smart_media.modelfields import SmartMediaField
from smart_media.signals import auto_purge_files_on_change, auto_purge_files_on_delete


class Product(models.Model):
    """
    Product of a Category.

    Attributes:
        category (models.ForeignKey): Required Assortment object.
        created (models.DateTimeField): Required creation datetime, automatically
            filled.
        title (models.CharField): Required unique title string.
        slug (models.CharField): Required unique slug string.
        description (models.TextField): Optional description long string.
        cover (SmartMediaField): Optional cover image file.
    """
    category = models.ForeignKey(
        "atoum.category",
        verbose_name="Related Category",
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(
        _("created on"),
        db_index=True,
        default=timezone.now,
    )
    title = models.CharField(
        _("title"),
        blank=False,
        max_length=100,
        default="",
        unique=True,
        # Unique for category ?
    )
    slug = models.CharField(
        _("slug"),
        blank=False,
        max_length=130,
        default="",
        unique=True,
        # Unique for category ?
    )
    description = models.TextField(
        _("description"),
        blank=True,
        default="",
    )
    cover = SmartMediaField(
        verbose_name=_("cover image"),
        upload_to="atoum/product/cover/%y/%m",
        max_length=255,
        blank=True,
        default="",
    )

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = [
            "title",
        ]

    def __str__(self):
        return self.title

    def disable_get_absolute_url(self):
        """
        NOTE: Disabled until view exist to avoid admin error 500
        Return absolute URL to the detail view.

        Returns:
            string: An URL.
        """
        return reverse("atoum:product-detail", args=[
            str(self.id)
        ])


# Connect some signals
post_delete.connect(
    auto_purge_files_on_delete(["cover"]),
    dispatch_uid="product_cover_on_delete",
    sender=Product,
    weak=False,
)
pre_save.connect(
    auto_purge_files_on_change(["cover"]),
    dispatch_uid="product_cover_on_change",
    sender=Product,
    weak=False,
)
