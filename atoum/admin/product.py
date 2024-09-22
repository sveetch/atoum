from django.contrib import admin

from smart_media.admin import SmartModelAdmin

from ..models import Product


@admin.register(Product)
class ProductAdmin(SmartModelAdmin):
    readonly_fields = ["created", "modified"]
    prepopulated_fields = {
        "slug": ("title",),
    }
