from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseBadRequest
from django.utils.html import format_html

from dal import autocomplete

from ..models import Assortment


class AssortmentAutocompleteView(UserPassesTestMixin, autocomplete.Select2QuerySetView):
    """
    View for Assortment autocompletion list with DAL.
    """
    def test_func(self):
        """
        Limit to admin only
        """
        return self.request.user.is_staff

    def get_queryset(self):
        """
        Build list queryset.

        Enable ``select_related`` on relation ``consumable`` because we intend to use
        it commonly in labels.
        """
        if not self.request.user.is_authenticated:
            return Assortment.objects.none()

        qs = Assortment.objects.all()

        if self.q:
            qs = qs.filter(title__istartswith=self.q).select_related("consumable")

        return qs.order_by(
            "consumable__title",
            "title"
        )

    def get_result_label(self, result):
        """
        Format a better list result display.
        """
        return format_html(
            "<small>{consumable}</small><br>{assortment}",
            consumable=result.consumable.title,
            assortment=result.title,
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
