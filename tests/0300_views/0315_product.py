from django.urls import reverse

from atoum.factories import (
    AssortmentFactory,
    CategoryFactory,
    ConsumableFactory,
    ProductFactory,
    UserFactory,
)


def test_autocomplete_authentication(client, db, settings):
    """
    Autocompletion backend view requires user to have staff level.
    """
    donald = UserFactory()
    picsou = UserFactory(flag_is_admin=True)

    url = reverse("atoum:autocomplete-products")

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


def test_autocomplete_post(admin_client, db, settings):
    """
    Autocompletion backend view does not allow POST request.
    """
    url = reverse("atoum:autocomplete-products")

    # POST request is forbidden
    response = admin_client.post(url, {"q": "Ping"}, HTTP_ACCEPT="application/json")
    assert response.status_code == 400


def test_autocomplete_backend(admin_client, db, settings):
    """
    Autocompletion backend view should return expected JSON payload
    """
    food = ConsumableFactory(title="Food")
    clothes = ConsumableFactory(title="Clothes")

    vegetable = AssortmentFactory(consumable=food, title="Vegetable")
    winter = AssortmentFactory(consumable=clothes, title="Winter")

    lettuce = CategoryFactory(assortment=vegetable, title="Lettuce")
    jacket = CategoryFactory(assortment=winter, title="Jacket")

    romaine = ProductFactory(category=lettuce, title="Romaine")
    arugula = ProductFactory(category=lettuce, title="Arugula")
    dufflecoat = ProductFactory(category=jacket, title="Duffle coat")

    url = reverse("atoum:autocomplete-products")
    response = admin_client.get(url)
    assert response.status_code == 200

    json_data = response.json()
    assert json_data["results"] == [
        {
            "id": str(dufflecoat.id),
            "text": "<small>Clothes &gt; Winter &gt; Jacket</small><br>Duffle coat",
            "selected_text": "Clothes &gt; Winter &gt; Jacket &gt; Duffle coat"
        },
        {
            "id": str(arugula.id),
            "text": "<small>Food &gt; Vegetable &gt; Lettuce</small><br>Arugula",
            "selected_text": "Food &gt; Vegetable &gt; Lettuce &gt; Arugula"
        },
        {
            "id": str(romaine.id),
            "text": "<small>Food &gt; Vegetable &gt; Lettuce</small><br>Romaine",
            "selected_text": "Food &gt; Vegetable &gt; Lettuce &gt; Romaine"
        }
    ]
