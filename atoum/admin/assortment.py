from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..models import Assortment


@admin.register(Assortment)
class AssortmentAdmin(admin.ModelAdmin):
    readonly_fields = ["created", "modified"]
    prepopulated_fields = {
        "slug": ("title",),
    }
    ordering = Assortment.COMMON_ORDER_BY
    search_fields = [
        "title",
    ]
    list_display = (
        "title",
        "consumable",
        "count_categories",
        "modified",
    )
    list_filter = (
        "consumable",
    )
    autocomplete_fields = ["consumable"]

    def count_categories(self, obj):
        """
        Count related categories.
        """
        return obj.category_set.count()
    count_categories.short_description = _("Categories")
