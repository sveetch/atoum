from django.urls import path

from .views import (
    RecursiveTreeView,
    DummyView,
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
]
