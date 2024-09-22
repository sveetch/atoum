from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone


class Assortment(models.Model):
    """
    Assortment of consumables.

    Attributes:
        consumable (models.ForeignKey): Required Consumable object.
        created (models.DateTimeField): Required creation datetime, automatically
            filled.
        title (models.CharField): Required unique title string.
        slug (models.CharField): Required unique slug string.
    """
    consumable = models.ForeignKey(
        "atoum.consumable",
        verbose_name="Related consumable",
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
    )
    slug = models.CharField(
        _("slug"),
        blank=False,
        max_length=130,
        default="",
        unique=True,
    )

    class Meta:
        verbose_name = _("Assortment")
        verbose_name_plural = _("Assortments")
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
        return reverse("atoum:assortment-detail", args=[
            str(self.id)
        ])
