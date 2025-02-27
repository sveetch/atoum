from django.http import Http404
from django.views.generic import TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..models import Shopping
from .mixins import AtoumBreadcrumMixin


class ShoppinglistDetailView(AtoumBreadcrumMixin, SingleObjectMixin, TemplateView):
    """
    Shopping list detail
    """
    template_name = "atoum/shopping/detail.html"
    context_object_name = "shopping_object"
    crumb_title = None  # No usage since title depends from object
    crumb_urlname = "atoum:shopping-list-detail"

    @property
    def crumbs(self):
        return [
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
            obj = Shopping.objects.filter(**{
                "pk": object_id,
            }).get()
        except Shopping.DoesNotExist:
            raise Http404(
                _("No {} found matching the query").format(
                    Shopping._meta.verbose_name
                )
            )

        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        return super().get(request, *args, **kwargs)
