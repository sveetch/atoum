from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    """
    Category of a consumable assortment.

    Attributes:
        assortment (models.ForeignKey): Required Assortment object.
        created (models.DateTimeField): Required creation datetime, automatically
            filled.
        modified (models.DateTimeField): Required creation datetime, automatically
            filled.
        title (models.CharField): Required unique title string.
        slug (models.CharField): Required unique slug string.
    """
    assortment = models.ForeignKey(
        "atoum.assortment",
        verbose_name=_("Assortment"),
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(
        _("creation date"),
        db_index=True,
        default=timezone.now,
    )
    modified = models.DateTimeField(
        _("modification date"),
        db_index=True,
        default=timezone.now,
    )
    title = models.CharField(
        _("title"),
        blank=False,
        max_length=100,
        default="",
    )
    slug = models.CharField(
        _("slug"),
        blank=False,
        max_length=130,
        default="",
    )

    COMMON_ORDER_BY = ["title"]
    """
    List of field order commonly used in frontend view/api
    """

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = [
            "title",
        ]
        constraints = [
            # Enforce unique couple assortment + title
            models.UniqueConstraint(
                fields=[
                    "assortment", "title"
                ],
                name="atoum_unique_cat_assortment_title"
            ),
            # Enforce unique couple assortment + slug
            models.UniqueConstraint(
                fields=[
                    "assortment", "slug"
                ],
                name="atoum_unique_cat_assortment_slug"
            ),
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
        return reverse("atoum:category-detail", args=[
            str(self.id)
        ])

    def save(self, *args, **kwargs):
        # Auto update 'modified' value on each save
        self.modified = timezone.now()

        super().save(*args, **kwargs)
