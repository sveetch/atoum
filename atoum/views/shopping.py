from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..models import Shopping
from .mixins import AtoumBreadcrumMixin


class ShoppinglistIndexView(AtoumBreadcrumMixin, ListView):
    """
    List of Shopping lists
    """
    model = Shopping
    template_name = "atoum/shopping/index.html"
    paginate_by = settings.ATOUM_SHOPPINGLIST_PAGINATION
    crumb_title = _("Shopping lists")
    crumb_urlname = "atoum:shopping-list-index"

    def get_queryset(self):
        # Append 'done' field over the common ordering fields so the undone lists
        # have higher priority
        ordering = ["done"] + self.model.COMMON_ORDER_BY
        return self.model.objects.order_by(*ordering)

    @property
    def crumbs(self):
        return [
            (
                ShoppinglistIndexView.crumb_title,
                reverse(ShoppinglistIndexView.crumb_urlname)
            ),
        ]


class ShoppinglistDetailView(AtoumBreadcrumMixin, SingleObjectMixin, TemplateView):
    """
    Shopping list detail
    """
    model = Shopping
    template_name = "atoum/shopping/detail.html"
    context_object_name = "shopping_object"
    crumb_title = None  # No usage since title depends from object
    crumb_urlname = "atoum:shopping-list-detail"

    @property
    def crumbs(self):
        return [
            (
                ShoppinglistIndexView.crumb_title,
                reverse(ShoppinglistIndexView.crumb_urlname)
            ),
            (
                str(self.object),
                reverse(self.crumb_urlname, kwargs={
                    "pk": self.object.id,
                })
            ),
        ]

    def get_object(self):
        """
        Get the Shopping list object
        """
        object_id = self.kwargs.get("pk")

        try:
            obj = Shopping.objects.filter(**{"pk": object_id}).get()
        except Shopping.DoesNotExist:
            msg = _("No {} found matching the query")
            raise Http404(msg.format(self.model._meta.verbose_name))

        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        return super().get(request, *args, **kwargs)


class ShoppinglistToggleSelectionView(SingleObjectMixin, View):
    """
    TODO: This currently only enable a selection, it should also be able to disable it
    so it will be a real 'toggle' view.

    TODO: Test coverage.
    """
    model = Shopping

    def get_object(self):
        """
        Get the Shopping list object
        """
        object_id = self.kwargs.get("pk")

        try:
            obj = Shopping.objects.filter(**{"pk": object_id}).get()
        except Shopping.DoesNotExist:
            msg = _("No {} found matching the query")
            raise Http404(msg.format(self.model._meta.verbose_name))

        return obj

    def get(self, request, *args, **kwargs):
        url = reverse("atoum:dashboard")

        # TODO: Ensure given url path is always safe
        if "next" in self.request.GET:
            url = self.request.GET.get("next")

        if "pk" in self.kwargs:
            self.object = self.get_object()

            self.request.session["atoum_shopping_selection"] = self.object.id
        else:
            del self.request.session["atoum_shopping_selection"]

        return HttpResponseRedirect(url)
