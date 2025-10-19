from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from dal import autocomplete

from ..models import Category, Product
from ..form_helpers import AdminProductFormHelper


class CategoryBreadcrumbChoiceField(forms.ModelChoiceField):
    """
    Customize category model choice field.
    """
    def label_from_instance(self, obj):
        """
        Display category parenting crumbs of a choice option.

        This label should be the same returned from
        ``CategoryAutocompleteView.get_selected_result_label()``.
        """
        return obj.parenting_crumbs_html()


class ProductAdminForm(autocomplete.FutureModelForm):
    class Meta:
        fields = "__all__"
        model = Product

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Override Category model form field to customize option label and enable
        # DAL autocompletion
        self.fields["category"] = CategoryBreadcrumbChoiceField(
            label=_("Category"),
            queryset=Category.objects.all().select_related(
                "assortment",
                "assortment__consumable"
            ),
            required=True,
            blank=False,
            widget=autocomplete.ModelSelect2(
                url="atoum:autocomplete-categories",
                attrs={"data-html": True},
            ),
        )


class ProductMoveToAdminForm(forms.Form):
    """
    Form for admin to assign a selection of objects to another relation.
    """
    # Limit is arbitrary, it may be computed on base of 'ModelAdmin.list_per_page'
    # multiplicated with limit of id allowed length plus the number of comma separators
    selection = forms.CharField(max_length=600, min_length=1, widget=forms.HiddenInput)
    destination = forms.ModelChoiceField(queryset=Category.objects.none())
    admin_filters = forms.CharField(
        max_length=600,
        required=False,
        widget=forms.HiddenInput,
    )

    def __init__(self, *args, **kwargs):
        self.products = kwargs.pop("products")
        self.admin_filters = kwargs.pop("admin_filters", "")

        super().__init__(*args, **kwargs)

        # Selection data is automatically computed from given objects
        self.fields["selection"].initial = ",".join([str(v.id) for v in self.products])
        self.fields["admin_filters"].initial = self.admin_filters

        # Destination is enhanced with a better option item label
        self.fields["destination"] = CategoryBreadcrumbChoiceField(
            label=_("Destination category"),
            queryset=Category.objects.all().select_related(
                "assortment",
                "assortment__consumable"
            ),
            required=True,
            blank=False,
            widget=autocomplete.ModelSelect2(
                url="atoum:autocomplete-categories",
                attrs={"data-html": True},
            ),
        )

        # Crispy form layout helper
        self.helper = AdminProductFormHelper()

    @property
    def media(self):
        """
        Define basic form medias as done in ``django.contrib.admin.options.ModelAdmin``.
        """
        media = super().media
        extra = "" if settings.DEBUG else ".min"
        css = [
            "forms.css",
        ]
        js = [
            "vendor/jquery/jquery%s.js" % extra,
            "jquery.init.js",
            "core.js",
            "admin/RelatedObjectLookups.js",
            "actions.js",
            "vendor/xregexp/xregexp%s.js" % extra,
            "cancel.js",
        ]

        return forms.Media(
            css={
                "all": ["admin/css/%s" % url for url in css],
            },
            js=["admin/js/%s" % url for url in js]
        ) + media

    def save(self, *args, **kwargs):
        self.products.update(category=self.cleaned_data["destination"])

        return len(self.products), str(self.cleaned_data["destination"])
