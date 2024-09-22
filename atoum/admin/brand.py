from django.contrib import admin

from smart_media.admin import SmartModelAdmin

from ..models import Brand


@admin.register(Brand)
class BrandAdmin(SmartModelAdmin):
    readonly_fields = ["created", "modified"]
    prepopulated_fields = {
        "slug": ("title",),
    }
