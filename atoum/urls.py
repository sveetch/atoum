from django.urls import path

from .views import (
    RecursiveTreeView,
    AssortmentAutocompleteView,
    CategoryAutocompleteView,
    DummyView,
    ProductAutocompleteView,
)


app_name = "atoum"


urlpatterns = [
    path("", RecursiveTreeView.as_view(), name="recursive-tree"),
    path(
        "assortments/<slug:slug>/",
        DummyView.as_view(),
        name="assortment-detail"
    ),
    path(
        "categories/<int:pk>/",
        DummyView.as_view(),
        name="category-detail"
    ),
    path(
        "consumables/<slug:slug>/",
        DummyView.as_view(),
        name="consumable-detail"
    ),
    path(
        "brands/<slug:slug>/",
        DummyView.as_view(),
        name="brand-detail"
    ),
    path(
        "brands/<slug:slug>/",
        DummyView.as_view(),
        name="brand-detail"
    ),
    path(
        "products/<slug:slug>/",
        DummyView.as_view(),
        name="product-detail"
    ),
    path(
        "autocomplete/assortments/",
        AssortmentAutocompleteView.as_view(),
        name="autocomplete-assortments",
    ),
    path(
        "autocomplete/categories/",
        CategoryAutocompleteView.as_view(),
        name="autocomplete-categories",
    ),
    path(
        "autocomplete/products/",
        ProductAutocompleteView.as_view(),
        name="autocomplete-products",
    ),
]
