from django.urls import reverse

from atoum.factories import (
    AssortmentFactory,
    CategoryFactory,
    ConsumableFactory,
    ProductFactory,
    UserFactory,
)
from atoum.utils.tests import html_pyquery

from tests.initial import initial_catalog  # noqa: F401


def test_index_empty(client, db):
    """
    Product index should just respond with an empty list.
    """
    url = reverse("atoum:product-index")
    response = client.get(url, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 200

    dom = html_pyquery(response)
    assert len(dom.find(".product-index .products .item")) == 0


def test_index_filled(client, db, initial_catalog):  # noqa: F811
    """
    Product index should list available assortments with pagination.
    """
    url = reverse("atoum:product-index")
    response = client.get(url, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 200

    dom = html_pyquery(response)
    titles = [
        v.cssselect(".parent")[0].text + ":" + v.cssselect(".title")[0].text
        for v in dom.find(".product-index .products .item")
    ]
    assert titles == [
        "Yellows:Corn",
        "Beef:Sensitive",
        "Beef:Steack",
        "Beef:T-Bone",
        "Reds:Tomatoe",
        "Beef:Tongue",
        "Chicken:Wing",
    ]


def test_detail_filled(admin_client, db, initial_catalog):  # noqa: F811
    """
    Product detail view should contain product detail informations.

    NOTE: We currently use admin_client since management links are restricted to
    staff user but in fact the whole app should be restricted to staff so there is no
    need to duplicate code to test with both lambda users and staff users.
    """
    tomatoe = initial_catalog.products["tomatoe"]
    url = reverse(
        "atoum:product-detail",
        kwargs={
            "consumable_slug": tomatoe.category.assortment.consumable.slug,
            "assortment_slug": tomatoe.category.assortment.slug,
            "category_slug": tomatoe.category.slug,
            "product_slug": tomatoe.slug,
        }
    )
    response = admin_client.get(url, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 200

    # There is currently no sensitive data on product detail so at least we check
    # about management links
    dom = html_pyquery(response)
    assert len(dom.find(".manage-object")) == 1

    management_links = [v.get("href") for v in dom.find(".manage-object a")]
    assert sorted(management_links) == [
        reverse("admin:atoum_product_change", kwargs={"object_id": tomatoe.id}),
        reverse("admin:atoum_product_delete", kwargs={"object_id": tomatoe.id}),
    ]


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


def test_autocomplete_post(admin_client, db):
    """
    Autocompletion backend view does not allow POST request.
    """
    url = reverse("atoum:autocomplete-products")

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
