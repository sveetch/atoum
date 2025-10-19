from django.contrib import admin
from django.urls import path, reverse
from django.http import HttpResponseRedirect, QueryDict
from django.utils.translation import gettext_lazy as _

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export import fields
from import_export.widgets import ForeignKeyWidget
from smart_media.admin import SmartAdminMixin

from ..forms import ProductAdminForm
from ..models import Category, Product
from ..views.admin import ProductActionMoveAdminView


class ProductResource(resources.ModelResource):
    """
    Data resource configuration for 'django-import-export'.
    """
    category = fields.Field(
        column_name="category",
        attribute="category",
        widget=ForeignKeyWidget(Category, field="title")
    )

    class Meta:
        model = "atoum.Product"
        fields = ("title", "slug", "category", "description")
        import_id_fields = ("slug",)


@admin.register(Product)
class ProductAdmin(SmartAdminMixin, ImportExportModelAdmin):
    """
    Model admin controller.
    """
    form = ProductAdminForm
    list_select_related = ["category"]
    readonly_fields = ["created", "modified"]
    prepopulated_fields = {
        "slug": ("title",),
    }
    ordering = Product.COMMON_ORDER_BY
    search_fields = [
        "title",
        "description",
    ]
    list_display = (
        "title",
        "category",
        "brand",
        "modified",
    )
    autocomplete_fields = ["brand"]
    list_filter = (
        "category",
        "brand",
    )
    resource_classes = [ProductResource]
    actions = ["move_to_category"]

    def get_urls(self):
        """
        Set some additional custom admin views
        """
        urls = super().get_urls()

        extra_urls = [
            path(
                "actions/move/",
                self.admin_site.admin_view(
                    ProductActionMoveAdminView.as_view(),
                ),
                name="atoum_admin_product_move",
            ),
        ]

        return extra_urls + urls

    @admin.action(description=_("Move selected products to a category"))
    def move_to_category(self, request, queryset):
        """
        Redirect to dedicated form view.

        Object id of selected products along admin changelist filters are passed into
        redirection.
        """
        selected = queryset.values_list("pk", flat=True)
        url = reverse("admin:atoum_admin_product_move")

        # Ensure changelist filters from GET request are passed to the view
        request_query = QueryDict(mutable=True)
        request_query.update(request.GET.dict())
        request_query.update({"selection": ",".join(str(pk) for pk in selected)})

        return HttpResponseRedirect(
            url + "?{}".format(request_query.urlencode(safe=","))
        )


class ProductAdminInline(admin.StackedInline):
    """
    Inline model admin controller to be used in other model admin controllers.
    """
    model = Product
    autocomplete_fields = ["category", "brand"]
    exclude = ["created", "modified", "description"]
    prepopulated_fields = {
        "slug": ("title",),
    }
    extra = 0
    can_delete = False
