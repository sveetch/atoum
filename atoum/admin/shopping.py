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

        TODO: When creating a new fresh Shopping object, if no items have been added
        the following cause the Shopping object to be directly marked as 'done'. It's
        not what would be expected, at least a new object without initial items should
        let it be 'undone'.
        """
        super().save_formset(request, form, formset, change)

        if (
            form.instance.done is False and
            ShoppingItem.objects.filter(shopping=form.instance, done=False).count() == 0
        ):
            # Items are allowed to make the shopping done if they are all done
            # themselves
            form.instance.done = True
            form.instance.save()
        elif (
            form.instance.done is True and
            ShoppingItem.objects.filter(shopping=form.instance, done=False).count() > 0
        ):
            # Items are allowed to make the shopping undone if one of them is undone
            form.instance.done = False
            form.instance.save()
