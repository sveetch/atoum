from .assortment import AssortmentAutocompleteView, AssortmentDetailView
from .category import CategoryAutocompleteView, CategoryDetailView
from .consumable import ConsumableDetailView, ConsumableIndexView
from .dashboard import DashboardView
from .dummy import DummyView
from .product import ProductAutocompleteView, ProductDetailView
from .tree import RecursiveTreeView


__all__ = [
    "AssortmentAutocompleteView",
    "AssortmentDetailView",
    "CategoryAutocompleteView",
    "CategoryDetailView",
    "ConsumableDetailView",
    "ConsumableIndexView",
    "DashboardView",
    "DummyView",
    "ProductAutocompleteView",
    "ProductDetailView",
    "RecursiveTreeView",
]
