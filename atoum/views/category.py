from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseBadRequest
from django.utils.html import format_html

from dal import autocomplete

from ..models import Category


class CategoryAutocompleteView(UserPassesTestMixin, autocomplete.Select2QuerySetView):
    """
    View for Category autocompletion list with DAL.
    """
    def test_func(self):
        """
        Limit to admin only
        """
        return self.request.user.is_staff

    def get_queryset(self):
        """
        Build list queryset.

        Enable ``select_related`` on relation ``assortment`` because we intend to use
        it commonly in labels.
        """
        if not self.request.user.is_authenticated:
            return Category.objects.none()

        qs = Category.objects.all()

        if self.q:
            qs = qs.filter(title__istartswith=self.q).select_related(
                "assortment",
                "assortment__consumable"
            )

        return qs.order_by(
            "assortment__consumable__title",
            "assortment__title",
            "title"
        )

    def get_result_label(self, result):
        """
        Format a better list result display.
        """
        return format_html(
            "<small>{consumable} &gt; {assortment}</small><br>{category}",
            consumable=result.assortment.consumable.title,
            assortment=result.assortment.title,
            category=result.title,
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
