from .assortment import (
    AssortmentAutocompleteView, AssortmentDetailView, AssortmentIndexView,
)
from .category import (
    CategoryAutocompleteView, CategoryDetailView, CategoryIndexView,
)
from .consumable import ConsumableDetailView, ConsumableIndexView
from .dashboard import DashboardView
from .dummy import DummyView
from .product import (
    ProductAutocompleteView, ProductDetailView, ProductIndexView,
)
from .tree import RecursiveTreeView


__all__ = [
    "AssortmentAutocompleteView",
    "AssortmentDetailView",
    "AssortmentIndexView",
    "CategoryAutocompleteView",
    "CategoryDetailView",
    "CategoryIndexView",
    "ConsumableDetailView",
    "ConsumableIndexView",
    "DashboardView",
    "DummyView",
    "ProductAutocompleteView",
    "ProductDetailView",
    "ProductIndexView",
    "RecursiveTreeView",
]
