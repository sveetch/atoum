from django.urls import reverse

from atoum.utils.tests import html_pyquery

from tests.initial import initial_catalog


def test_index_empty(client, db):
    """
    Consumable index should just respond with an empty list.
    """
    url = reverse("atoum:consumable-index")
    response = client.get(url, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 200

    dom = html_pyquery(response)
    assert len(dom.find(".consumable-index .consumables .item")) == 0


def test_index_filled(client, db, initial_catalog):
    """
    Consumable index should list all available consumables.
    """
    url = reverse("atoum:consumable-index")
    response = client.get(url, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 200

    dom = html_pyquery(response)
    titles = [v.text for v in dom.find(".consumable-index .consumables .item .title")]
    assert titles == ["Food", "Hygiene", "Pets"]
