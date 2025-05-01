from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from haystack.query import RelatedSearchQuerySet
from haystack.generic_views import SearchView

from ..forms import GlobalSearchForm
from .mixins import AtoumBreadcrumMixin


class GlobalSearchView(AtoumBreadcrumMixin, LoginRequiredMixin, SearchView):
    """
    View to implement search for indexed Atoum models.
    """
    template_name = "atoum/search/results.html"
    form_class = GlobalSearchForm
    crumb_title = _("Search")
    crumb_urlname = "atoum:search-results"

    @property
    def crumbs(self):
        return [
            (self.crumb_title, reverse(self.crumb_urlname)),
        ]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if self.request.method == "GET":
            # Add some arguments to notify some fields are empty
            # TODO: Usage of these args (from the crispy layout) should have a test
            # coverage
            kwargs.update({
                "empty_query": not self.request.GET.get("q"),
                "empty_models": not self.request.GET.get("models"),
            })

        return kwargs

    def get_queryset(self):
        """
        Use a ``RelatedSearchQuerySet`` so we can use ``select_related()`` when loading
        model objects from search results.
        """
        if self.queryset is None:
            self.queryset = RelatedSearchQuerySet()
        return self.queryset
