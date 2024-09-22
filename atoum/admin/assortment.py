from django.contrib import admin

from ..models import Assortment


@admin.register(Assortment)
class AssortmentAdmin(admin.ModelAdmin):
    readonly_fields = ["created", "modified"]
    prepopulated_fields = {
        "slug": ("title",),
    }
