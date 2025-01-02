from django.contrib import admin

from smart_media.admin import SmartModelAdmin

from ..models import Product


@admin.register(Product)
class ProductAdmin(SmartModelAdmin):
    list_select_related = ["category"]
    readonly_fields = ["created", "modified"]
    prepopulated_fields = {
        "slug": ("title",),
    }
    ordering = Product.COMMON_ORDER_BY
    search_fields = [
        "title",
        "description",
    ]
    list_display = (
        "title",
        "category",
        "brand",
        "modified",
    )
    autocomplete_fields = ["category", "brand"]
    list_filter = (
        "category",
        "brand",
    )


class ProductInline(admin.StackedInline):
    model = Product
    autocomplete_fields = ["category", "brand"]
    exclude = ["created", "modified", "description"]
    prepopulated_fields = {
        "slug": ("title",),
    }
    extra = 0
    can_delete = False
