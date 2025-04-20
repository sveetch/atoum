from django.urls import reverse

from atoum.utils.tests import html_pyquery

from tests.initial import initial_catalog  # noqa: F401


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


def test_index_filled(client, db, initial_catalog,  # noqa: F811
                      django_assert_num_queries):
    """
    Consumable index should list all available consumables.
    """
    url = reverse("atoum:consumable-index")

    # Only a single queryset to list objects
    with django_assert_num_queries(1):
        response = client.get(url, follow=True)

    assert response.redirect_chain == []
    assert response.status_code == 200

    dom = html_pyquery(response)
    titles = [v.text for v in dom.find(".consumable-index .consumables .item .title")]
    assert titles == ["Food (3)", "Hygiene (0)", "Other consumable (1)", "Pets (1)"]


def test_detail_filled(client, db, initial_catalog,  # noqa: F811
                       django_assert_num_queries):
    """
    Consumable detail should list its related assortments.
    """
    foods = initial_catalog.consumables["foods"]
    url = reverse("atoum:consumable-detail", kwargs={"slug": foods.slug})

    # A queryset for the main object, another one to list its related objects and
    # another one for pagination
    with django_assert_num_queries(3):
        response = client.get(url, follow=True)

    assert response.redirect_chain == []
    assert response.status_code == 200

    dom = html_pyquery(response)
    titles = [
        v.text
        for v in dom.find(".consumable-detail .consumable-assortments .item .title")
    ]
    assert titles == ["Meats (3)", "Sweat treats (0)", "Vegetables (2)"]
