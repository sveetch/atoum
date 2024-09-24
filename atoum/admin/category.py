from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ["created", "modified"]
    prepopulated_fields = {
        "slug": ("title",),
    }
    ordering = Category.COMMON_ORDER_BY
    search_fields = [
        "title",
    ]
    list_display = (
        "title",
        "assortment",
        "count_products",
        "modified",
    )
    list_filter = (
        "assortment",
    )
    autocomplete_fields = ["assortment"]

    def count_products(self, obj):
        """
        Count related products.
        """
        return obj.product_set.count()
    count_products.short_description = _("Products")
