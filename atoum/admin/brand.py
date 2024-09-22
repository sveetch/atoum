from django.contrib import admin

from ..models import Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    readonly_fields = ["created", "modified"]
