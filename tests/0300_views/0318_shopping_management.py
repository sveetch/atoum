from django.urls import reverse

import pytest
from freezegun import freeze_time

from atoum.utils.tests import html_pyquery
from atoum.factories import ShoppingFactory

from tests.initial import initial_catalog  # noqa: F401


@pytest.mark.skip("Build response template with tags and partials before")
def test_post_add(client, db, initial_catalog):
    """
    View assumes a POST request for a product that is not already in the Shopping list
    to be an addition
    """
    shopping = ShoppingFactory(fill_products=[
        (initial_catalog.products["corn"], {"quantity": 1}),
        (initial_catalog.products["steack"], {"quantity": 1, "done": True}),
        (initial_catalog.products["tomatoe"], {"quantity": 42}),
    ])

    url = reverse("atoum:shopping-list-product", kwargs={
        "pk": shopping.id,
        "product_id": initial_catalog.products["wing"].id,
    })
    response = client.post(url, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 200
