from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseBadRequest
from django.utils.html import format_html

from dal import autocomplete

from ..models import Product


class ProductAutocompleteView(UserPassesTestMixin, autocomplete.Select2QuerySetView):
    """
    View for Product autocompletion list with DAL.
    """
    def test_func(self):
        """
        Limit to admin only
        """
        return self.request.user.is_staff

    def get_queryset(self):
        """
        Build list queryset.

        Enable ``select_related`` on deep relations.
        """
        if not self.request.user.is_authenticated:
            return Product.objects.none()

        qs = Product.objects.all()

        if self.q:
            qs = qs.filter(title__istartswith=self.q).select_related(
                "category",
                "category_assortment",
                "category_assortment__consumable"
            )

        return qs.order_by(
            "category__assortment__consumable__title",
            "category__assortment__title",
            "category__title",
            "title"
        )

    def get_result_label(self, result):
        """
        Format a better list result display.
        """
        template = (
            "<small>{consumable} &gt; {assortment} &gt; {category}</small><br>{product}"
        )
        return format_html(
            template,
            consumable=result.category.assortment.consumable.title,
            assortment=result.category.assortment.title,
            category=result.category.title,
            product=result.title,
        )

    def get_selected_result_label(self, result):
        """
        Format a better selected result display.
        """
        return result.parenting_crumbs_html()

    def post(self, request, *args, **kwargs):
        """
        POST request is forbidden since DAL would allow creation of new object for a
        missing value and we don't want it.
        """
        return HttpResponseBadRequest()
