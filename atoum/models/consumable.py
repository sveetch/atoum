from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone


class Consumable(models.Model):
    """
    The very top level of consumable classification.

    Attributes:
        created (models.DateTimeField): Required creation datetime, automatically
            filled.
        title (models.CharField): Required unique title string.
        slug (models.CharField): Required unique slug string.
    """
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
    )
    slug = models.CharField(
        _("slug"),
        blank=False,
        max_length=130,
        default="",
        unique=True,
    )

    class Meta:
        verbose_name = _("Consumable")
        verbose_name_plural = _("Consumables")
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
        return reverse("atoum:consumable-detail", args=[
            str(self.id)
        ])
