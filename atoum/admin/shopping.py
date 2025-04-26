from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..forms import ShoppingAdminForm, ShoppingItemInlineForm
from ..models import Shopping, ShoppingItem


class ShoppingItemInlineAdmin(admin.StackedInline):
    """
    Inline model admin controller for 'ShoppingItem' to be used in other model admin
    controllers.
    """
    form = ShoppingItemInlineForm
    model = ShoppingItem
    exclude = ["created", "modified"]
    extra = 0
    can_delete = True


@admin.register(Shopping)
class ShoppingAdmin(admin.ModelAdmin):
    """
    Model admin controller for 'Shopping'.
    """
    form = ShoppingAdminForm
    inlines = [
        ShoppingItemInlineAdmin,
    ]
    readonly_fields = ["created"]
    search_fields = [
        "title",
    ]
    list_display = (
        "get_title",
        "created",
        "planning",
        "done",
    )

    def get_title(self, obj):
        """
        Count related assortments.
        """
        return str(obj)
    get_title.short_description = _("Title")

    def save_formset(self, request, form, formset, change):
        """
        Customize inlines item saving (because it can not be done on the inline form
        itself).
        """
        super().save_formset(request, form, formset, change)

        form.instance.update_shopping_done()
