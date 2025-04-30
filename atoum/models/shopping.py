from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone
from django.utils.dateformat import format as date_format
from django.utils.functional import cached_property
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
        Return a queryset for all ShoppingItem objects in a single query.

        .. Warning::
            This method is not cached and therefore will spawn a new queryset each time
            it is called. If you don't need to update Shopping or its item during the
            same thread, prefer to use property ``FOOOOO`` instead that is cached and
            avoid multiple querysets to get items on different operation during the
            same thread.

        Returns:
            queryset: All ShoppingItem objects related to the Shopping object.
        """
        return ShoppingItem.objects.filter(shopping=self).select_related(
            *self.HIERARCHY_SELECT_RELATED
        )

    @cached_property
    def current_items(self):
        """
        Get the current related ShoppingItem objects.

        This method is cached, once called its results will never change no matter
        you are updating the Shopping or its item objects.

        Returns:
            queryset: Queryset of ShoppingItem related to the Shopping object.
        """
        return self.get_items()

    @cached_property
    def current_item_ids(self):
        """
        Return a tuple of related ShoppingItem object ids.

        Depends on cached property ``Shopping.current_items``.

        Returns:
            tuple: Tuple of ShoppingItem ids.
        """
        return tuple([v.product.id for v in self.current_items])

    def is_product_shopped(self, product):
        """
        Check if given Product is an item of the Shopping object.

        Depends on cached property ``Shopping.current_items``.

        Arguments:
            product (atoum.models.Product): Product object.

        Returns:
            boolean: True if product is in list else None.
        """
        return product.id in self.current_item_ids

    def item_for_product(self, product):
        """
        Return the shopping item for a product in shopping list.

        Depends on cached property ``Shopping.current_items``.

        Arguments:
            product (atoum.models.Product): Product object.

        Returns:
            ShoppingItem: The item object for given Product if it is an item of the
            Shopping object else it returns ``None``.
        """
        if self.is_product_shopped(product):
            for item in self.current_items:
                if item.product.id == product.id:
                    return item

        return None

    def quantity_for_product(self, product):
        """
        Return the saved item quantity for the given Product.

        Depends on cached property ``Shopping.current_items``.

        Arguments:
            product (atoum.models.Product): Product object.

        Returns:
            integer: The quantity of Product if it is an item of the Shopping object
            else it returns ``None``.
        """
        item = self.item_for_product(product)

        return item.quantity if item else None

    def update_shopping_done(self, commit=True):
        """
        Update the field ``done`` of a Shopping object depending its current value and
        its items.

        TODO: When creating a new fresh Shopping object, if no items have been added
        the following cause the Shopping object to be directly marked as 'done'. It's
        not what would be expected, at least a new object without initial items should
        let it be 'undone'.

        Returns:
            boolean: True if an update of ``done`` value has been done else False.
        """
        new_value = None

        # Items are allowed to make the shopping done if they are all done themselves
        if (
            self.done is False and
            ShoppingItem.objects.filter(shopping=self, done=False).count() == 0
        ):
            new_value = True
        # Items are allowed to make the shopping undone if at least one of them is
        # undone
        elif (
            self.done is True and
            ShoppingItem.objects.filter(shopping=self, done=False).count() > 0
        ):
            new_value = False

        if new_value is not None:
            self.done = new_value

            if commit:
                self.save()

        return new_value

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
