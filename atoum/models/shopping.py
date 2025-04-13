from dataclasses import dataclass, field as dataclass_field

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone
from django.utils.dateformat import format as date_format
from django.utils.text import capfirst


class Shopping(models.Model):
    """
    Shopping object to gather choices of products.

    Attributes:
        created (models.DateTimeField): Required creation datetime, automatically
            filled.
        planning (models.DateTimeField): Required planning datetime, automatically
            filled.
        title (models.CharField): Optional title string.
        done (models.CharField): Optional boolean.
        products (models.ManyToManyField): Optional product selection
    """
    created = models.DateTimeField(
        _("creation date"),
        db_index=True,
        default=timezone.now,
    )
    planning = models.DateTimeField(
        _("planning date"),
        db_index=True,
        default=timezone.now,
    )
    title = models.CharField(
        _("title"),
        blank=True,
        max_length=100,
        default="",
    )
    done = models.BooleanField(
        verbose_name=_("done"),
        default=False,
        blank=True,
    )
    products = models.ManyToManyField(
        "atoum.Product",
        verbose_name=_("items"),
        related_name="shoppings",
        blank=True,
        through="atoum.ShoppingItem",
        through_fields=("shopping", "product"),
    )

    COMMON_ORDER_BY = ["-planning"]
    """
    List of field order commonly used in frontend view/api
    """

    HIERARCHY_SELECT_RELATED = [
        "product",
        "product__category",
        "product__category__assortment",
        "product__category__assortment__consumable",
    ]
    """
    List of foreign-key relationships field names to "follow" in queryset to avoid
    multiple queries. Commonly used in a ``Queryset.select_related()``.
    """

    class Meta:
        verbose_name = _("Shopping")
        verbose_name_plural = _("Shoppings")
        ordering = [
            "title",
        ]

    def __str__(self):
        """
        Display title if not empty else the creation date.
        """
        return self.title or capfirst(date_format(self.created, "l d F Y"))

    def get_absolute_url(self):
        """
        Return absolute URL to the detail view.

        Returns:
            string: An URL.
        """
        return reverse("atoum:shopping-list-detail", args=[self.id])

    def get_status(self):
        """
        Get a status computed from 'done' state and number of done items.

        Returns:
            dict:
        """
        computed = _("done") if self.done is True else _("open")
        states = self.shoppingitem_set.values_list(
            "done",
            flat=True
        )
        dones = len([v for v in states if v is True])

        computed = "open"
        if self.done is True:
            computed = "done"
        elif dones > 0:
            computed = "ongoing"

        return {
            "status": computed,
            "dones": dones,
            "opens": len([v for v in states if v is False]),
        }

    def get_items(self):
        """
        Return a queryset for all Shopping item objects in a single query.

        Returns:
            queryset: All ShoppingItem objects related to the Shopping object.
        """
        return ShoppingItem.objects.filter(shopping=self).select_related(
            *self.HIERARCHY_SELECT_RELATED
        )

    def save(self, *args, **kwargs):
        # Auto update 'modified' value on each save
        self.modified = timezone.now()

        super().save(*args, **kwargs)


class ShoppingItem(models.Model):
    """
    Shopping list item object.

    .. todo::
        Quantity value may be a choice field if product unit was a volume or weight.

    Attributes:
        created (models.DateTimeField): Required creation datetime, automatically
            filled.
        shopping (atoum.models.Shopping): Required
        product (atoum.models.Product): Required
        quantity (models.PositiveSmallIntegerField): Required positive small integer.
        done (models.CharField): Optional boolean.
    """
    created = models.DateTimeField(
        _("creation date"),
        default=timezone.now,
    )
    shopping = models.ForeignKey(
        "atoum.Shopping",
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        "atoum.Product",
        on_delete=models.CASCADE
    )
    quantity = models.PositiveSmallIntegerField(_("quantity"))
    done = models.BooleanField(
        verbose_name=_("done"),
        default=False,
        blank=True,
    )

    class Meta:
        verbose_name = _("Shopping item")
        verbose_name_plural = _("Shopping items")
        ordering = ["shopping", "product"]
        constraints = [
            # Enforce unique couple shopping + product
            models.UniqueConstraint(
                fields=[
                    "shopping", "product"
                ],
                name="atoum_unique_shoppingitem_shopping_product"
            ),
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


@dataclass
class ShoppingListInventory:
    """
    A simple dataclass to carry a Shopping list.

    It is especially used to provide an opened Shopping list in template context with
    its related products loaded in a single place to ensure no duplicate queries are
    performed.
    """
    obj: type(Shopping)
    items: list = dataclass_field(default_factory=list)
    item_ids: tuple = dataclass_field(default_factory=tuple, init=False)

    def __post_init__(self):
        if not self.items:
            self.items = self.obj.get_items()

        self.item_ids = tuple([v.product.id for v in self.items])

    def is_product_selected(self, product):
        """
        Check if product is in Shopping list.

        Arguments:
            product (atoum.models.Product): Product object.

        Returns:
            boolean: True if product is in list else None.
        """
        return product.id in self.item_ids

    def quantity_for_product(self, product):
        """
        Return the saved quantity for a product in shopping list.

        Arguments:
            product (atoum.models.Product): Product object.

        Returns:
            integer: The quantity of product if in list else None.
        """
        if self.is_product_selected(product):
            for item in self.items:
                if item.product.id == product.id:
                    return item.product.quantity

        return None
