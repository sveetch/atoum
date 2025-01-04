from django.contrib import admin

from ..forms import ShoppingItemInlineForm
from ..models import Shopping, ShoppingItem


class ShoppingItemInlineAdmin(admin.StackedInline):
    form = ShoppingItemInlineForm
    model = ShoppingItem
    exclude = ["created", "modified"]
    extra = 0
    can_delete = True


@admin.register(Shopping)
class ShoppingAdmin(admin.ModelAdmin):
    inlines = [
        ShoppingItemInlineAdmin,
    ]
