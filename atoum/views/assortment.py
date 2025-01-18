from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404, HttpResponseBadRequest
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from dal import autocomplete

from ..models import Assortment
from .dashboard import DashboardView
from .consumable import ConsumableIndexView, ConsumableDetailView
from .mixins import AtoumBreadcrumMixin


class AssortmentDetailView(AtoumBreadcrumMixin, SingleObjectMixin, ListView):
    """
    Assortment detail and its related category list
    """
    template_name = "atoum/assortment/detail.html"
    paginate_by = settings.CATEGORY_PAGINATION
    context_object_name = "assortment_object"
    crumb_title = None  # No usage since title depends from object
    crumb_urlname = "atoum:assortment-detail"

    @property
    def crumbs(self):
        return [
            (
                DashboardView.crumb_title,
                reverse(DashboardView.crumb_urlname)
            ),
            (
                ConsumableIndexView.crumb_title,
                reverse(ConsumableIndexView.crumb_urlname)
            ),
            (
                self.object.consumable.title,
                reverse(ConsumableDetailView.crumb_urlname, kwargs={
                    "slug": self.object.consumable.slug,
                })
            ),
            (
                self.object.title,
                reverse(self.crumb_urlname, kwargs={
                    "consumable_slug": self.object.consumable.slug,
                    "assortment_slug": self.object.slug,
                })
            ),
        ]

    def get_queryset(self):
        """
        Queryset to list sub relations
        """
        return self.object.category_set.order_by("title")

    def get_object(self):
        """
        Get the Assortment object for details
        """
        consumable_slug = self.kwargs.get("consumable_slug")
        assortment_slug = self.kwargs.get("assortment_slug")

        try:
            obj = Assortment.objects.filter(**{
                "consumable__slug": consumable_slug,
                "slug": assortment_slug,
            }).select_related("consumable").get()
        except Assortment.DoesNotExist:
            raise Http404(
                _("No {} found matching the query").format(
                    Assortment._meta.verbose_name
                )
            )

        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        return super().get(request, *args, **kwargs)


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
