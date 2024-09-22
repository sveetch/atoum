from django.contrib import admin

from ..models import Consumable


@admin.register(Consumable)
class ConsumableAdmin(admin.ModelAdmin):
    readonly_fields = ["created", "modified"]
