from django.urls import reverse

from atoum.factories import (
    AssortmentFactory,
    CategoryFactory,
    ConsumableFactory,
    UserFactory,
)
from atoum.utils.tests import html_pyquery

from tests.initial import initial_catalog  # noqa: F401


def test_anonymous(client, db, settings):
    """
    Anonymous are not allowed and is redirect to login.
    """
    url = reverse("atoum:category-index")
    response = client.get(url, follow=True)
    assert response.redirect_chain == [
        ("{}?next={}".format(settings.LOGIN_URL, url), 302),
    ]
    assert response.status_code == 200

    category = CategoryFactory()
    url = reverse("atoum:category-detail", kwargs={
        "consumable_slug": category.assortment.consumable.slug,
        "assortment_slug": category.assortment.slug,
        "category_slug": category.slug,
    })
    response = client.get(url, follow=True)
    assert response.redirect_chain == [
        ("{}?next={}".format(settings.LOGIN_URL, url), 302),
    ]
    assert response.status_code == 200


def test_index_empty(client, db):
    """
    Category index should just respond with an empty list.
    """
    client.force_login(UserFactory())

    url = reverse("atoum:category-index")
    response = client.get(url, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 200

    dom = html_pyquery(response)
    assert len(dom.find(".category-index .categories .item")) == 0


def test_index_filled(client, db, initial_catalog,  # noqa: F811
                      django_assert_num_queries):
    """
    Category index should list available assortments with pagination.
    """
    client.force_login(UserFactory())

    url = reverse("atoum:category-index")

    # Only a count queryset from pagination and the other one to list objects with
    # their relation preloaded
    with django_assert_num_queries(4):
        response = client.get(url, follow=True)

    assert response.redirect_chain == []
    assert response.status_code == 200

    dom = html_pyquery(response)
    titles = [
        v.cssselect(".parent")[0].text + ":" + v.cssselect(".title")[0].text
        for v in dom.find(".category-index .categories .item")
    ]
    assert titles == [
        "Meats:Beef (3)",
        "Croquettes:Beef (1)",
        "Meats:Chicken (1)",
        "Other assortment:Other category (1)",
        "Meats:Pig (0)",
        "Vegetables:Reds (1)",
        "Vegetables:Yellows (1)",
    ]


def test_detail_filled(client, db, initial_catalog,  # noqa: F811
                       django_assert_num_queries):
    """
    Category detail should list its related products.
    """
    client.force_login(UserFactory())

    beeffoods = initial_catalog.categories["beeffoods"]
    url = reverse(
        "atoum:category-detail",
        kwargs={
            "consumable_slug": beeffoods.assortment.consumable.slug,
            "assortment_slug": beeffoods.assortment.slug,
            "category_slug": beeffoods.slug,
        }
    )

    # A queryset for the main object, another one to list its related objects and
    # another one for pagination
    with django_assert_num_queries(5):
        response = client.get(url, follow=True)

    assert response.redirect_chain == []
    assert response.status_code == 200

    dom = html_pyquery(response)
    titles = [
        v.cssselect(".title")[0].text
        for v in dom.find(".category-detail .category-products .item .content")
    ]
    assert titles == ["Steack", "T-Bone", "Tongue"]


def test_autocomplete_authentication(client, db, settings):
    """
    Autocompletion backend view requires user to have staff level.
    """
    donald = UserFactory()
    picsou = UserFactory(flag_is_admin=True)

    url = reverse("atoum:autocomplete-categories")

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
    url = reverse("atoum:autocomplete-categories")

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

    url = reverse("atoum:autocomplete-categories")
    response = admin_client.get(url)
    assert response.status_code == 200

    json_data = response.json()
    assert json_data["results"] == [
        {
            "id": str(jacket.id),
            "text": "<small>Clothes &gt; Winter</small><br>Jacket",
            "selected_text": "Clothes &gt; Winter &gt; Jacket"
        },
        {
            "id": str(lettuce.id),
            "text": "<small>Food &gt; Vegetable</small><br>Lettuce",
            "selected_text": "Food &gt; Vegetable &gt; Lettuce"
        },
    ]
