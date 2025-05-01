from django.urls import reverse

from atoum.factories import ConsumableFactory, UserFactory
from atoum.utils.tests import html_pyquery

from tests.initial import initial_catalog  # noqa: F401


def test_anonymous(client, db, settings):
    """
    Anonymous are not allowed and is redirect to login.
    """
    url = reverse("atoum:consumable-index")
    response = client.get(url, follow=True)
    assert response.redirect_chain == [
        ("{}?next={}".format(settings.LOGIN_URL, url), 302),
    ]
    assert response.status_code == 200

    consumable = ConsumableFactory()
    url = reverse("atoum:consumable-detail", kwargs={"slug": consumable.slug})
    response = client.get(url, follow=True)
    assert response.redirect_chain == [
        ("{}?next={}".format(settings.LOGIN_URL, url), 302),
    ]
    assert response.status_code == 200


def test_index_empty(client, db):
    """
    Consumable index should just respond with an empty list.
    """
    client.force_login(UserFactory())

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
    client.force_login(UserFactory())

    url = reverse("atoum:consumable-index")

    with django_assert_num_queries(3):
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
    client.force_login(UserFactory())

    foods = initial_catalog.consumables["foods"]
    url = reverse("atoum:consumable-detail", kwargs={"slug": foods.slug})

    with django_assert_num_queries(5):
        response = client.get(url, follow=True)

    assert response.redirect_chain == []
    assert response.status_code == 200

    dom = html_pyquery(response)
    titles = [
        v.text
        for v in dom.find(".consumable-detail .consumable-assortments .item .title")
    ]
    assert titles == ["Meats (3)", "Sweat treats (0)", "Vegetables (2)"]
