from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..forms import CategoryAdminForm
from ..models import Category
from .product import ProductAdminInline


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_select_related = ["assortment"]
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
    inlines = [
        ProductAdminInline,
    ]

    def count_products(self, obj):
        """
        Count related products.
        """
        return obj.product_set.count()
    count_products.short_description = _("Products")


class CategoryInline(admin.StackedInline):
    model = Category
    exclude = ["created", "modified"]
    prepopulated_fields = {
        "slug": ("title",),
    }
    extra = 0
    can_delete = False
