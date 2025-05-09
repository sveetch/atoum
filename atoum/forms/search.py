from haystack.forms import ModelSearchForm

from ..models import Assortment, Category, Product
from ..form_helpers import AdvancedSearchFormHelper
from ..utils.text import normalize_text


class GlobalSearchForm(ModelSearchForm):
    """
    Form to search on all enabled Atoum models.
    """

    def __init__(self, *args, **kwargs):
        empty_query = kwargs.pop("empty_query", False)
        empty_models = kwargs.pop("empty_models", False)

        super().__init__(*args, **kwargs)

        # We don't want label since we use a group inline layout
        self.fields["q"].label = False
        self.fields["models"].label = False

        self.helper = AdvancedSearchFormHelper(
            empty_query=empty_query,
            empty_models=empty_models,
        )

    def search(self):
        """
        We don't keep the base queryset from inherit ModelSearchForm since it starts
        with an 'auto_query' that is not efficient with partial search. However this
        drops the feature of some operator like ``-`` to negate keywords.
        """
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get("q"):
            return self.no_query_found()

        # Search on main content with normalized query
        sqs = self.searchqueryset.filter(text=normalize_text(self.cleaned_data["q"]))

        # Enable all discovered model indexes from enabled applications
        sqs = sqs.models(*self.get_models())

        if self.load_all:
            # Get model objects from search result references
            sqs = sqs.load_all()

            # Define Assortment relationships to select in queryset instead of getting
            # them on their own querysets
            sqs = sqs.load_all_queryset(
                Assortment,
                Assortment.objects.all().select_related(
                    *Assortment.HIERARCHY_SELECT_RELATED
                )
            )

            # Define Category relationships to select
            sqs = sqs.load_all_queryset(
                Category,
                Category.objects.all().select_related(
                    *Category.HIERARCHY_SELECT_RELATED
                )
            )

            # Define Product relationships to select
            sqs = sqs.load_all_queryset(
                Product,
                Product.objects.all().select_related(
                    *Product.HIERARCHY_SELECT_RELATED
                )
            )

        return sqs
