from django.urls import reverse

from atoum.factories import (
    AssortmentFactory,
    ConsumableFactory,
    UserFactory,
)
from atoum.utils.tests import html_pyquery

from tests.initial import initial_catalog  # noqa: F401


def test_index_empty(client, db):
    """
    Assortment index should just respond with an empty list.
    """
    url = reverse("atoum:assortment-index")
    response = client.get(url, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 200

    dom = html_pyquery(response)
    assert len(dom.find(".assortment-index .assortments .item")) == 0


def test_index_filled(client, db, initial_catalog):  # noqa: F811
    """
    Assortment index should list available assortments with pagination.
    """
    url = reverse("atoum:assortment-index")
    response = client.get(url, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 200

    dom = html_pyquery(response)
    titles = [
        v.cssselect(".parent")[0].text + ":" + v.cssselect(".title")[0].text
        for v in dom.find(".assortment-index .assortments .item .body")
    ]
    assert titles == [
        "Pets:Croquettes",
        "Food:Meats",
        "Other consumable:Other assortment",
        "Food:Sweat treats",
        "Food:Vegetables",
    ]


def test_detail_filled(client, db, initial_catalog):  # noqa: F811
    """
    Assortment detail should list its related categories.
    """
    meats = initial_catalog.assortments["meats"]
    url = reverse(
        "atoum:assortment-detail",
        kwargs={
            "consumable_slug": meats.consumable.slug,
            "assortment_slug": meats.slug,
        }
    )
    response = client.get(url, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 200

    dom = html_pyquery(response)
    titles = [
        v.text
        for v in dom.find(".assortment-detail .assortment-categories .item .title")
    ]
    assert titles == ["Beef", "Chicken", "Pig"]


def test_autocomplete_authentication(client, db, settings):
    """
    Autocompletion backend view requires user to have staff level.
    """
    donald = UserFactory()
    picsou = UserFactory(flag_is_admin=True)

    url = reverse("atoum:autocomplete-assortments")

    # Anonymous is redirected to login form
    response = client.get(url, follow=True)
    assert response.redirect_chain == [
        ("{}?next={}".format(settings.LOGIN_URL, url), 302),
    ]
    assert response.status_code == 200

    # Authenticated user without any permissions is not authorized
    client.force_login(donald)
    response = client.get(url, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 403

    # Authenticated user with staff level is authorized
    client.force_login(picsou)
    response = client.get(url, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 200


def test_autocomplete_post(admin_client, db):
    """
    Autocompletion backend view does not allow POST request.
    """
    url = reverse("atoum:autocomplete-assortments")

    # POST request is forbidden
    response = admin_client.post(url, {"q": "Ping"}, HTTP_ACCEPT="application/json")
    assert response.status_code == 400


def test_autocomplete_backend(admin_client, db):
    """
    Autocompletion backend view should return expected JSON payload
    """
    food = ConsumableFactory(title="Food")
    clothes = ConsumableFactory(title="Clothes")

    vegetable = AssortmentFactory(consumable=food, title="Vegetable")
    winter = AssortmentFactory(consumable=clothes, title="Winter")

    url = reverse("atoum:autocomplete-assortments")
    response = admin_client.get(url)
    assert response.status_code == 200

    json_data = response.json()
    assert json_data["results"] == [
        {
            "id": str(winter.id),
            "text": "<small>Clothes</small><br>Winter",
            "selected_text": "Clothes &gt; Winter"
        },
        {
            "id": str(vegetable.id),
            "text": "<small>Food</small><br>Vegetable",
            "selected_text": "Food &gt; Vegetable"
        },
    ]
