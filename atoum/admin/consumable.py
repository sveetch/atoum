from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..models import Consumable
from .assortment import AssortmentInline


@admin.register(Consumable)
class ConsumableAdmin(admin.ModelAdmin):
    readonly_fields = ["created", "modified"]
    prepopulated_fields = {
        "slug": ("title",),
    }
    ordering = Consumable.COMMON_ORDER_BY
    search_fields = [
        "title",
    ]
    list_display = (
        "title",
        "count_assortments",
        "modified",
    )
    inlines = [
        AssortmentInline,
    ]

    def count_assortments(self, obj):
        """
        Count related assortments.
        """
        return obj.assortment_set.count()
    count_assortments.short_description = _("Assortments")
