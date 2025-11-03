import datetime
from zoneinfo import ZoneInfo

from django.urls import reverse

from freezegun import freeze_time

from atoum.utils.tests import html_pyquery
from atoum.factories import ShoppingFactory, UserFactory

from tests.initial import initial_catalog  # noqa: F401


def test_index_anonymous(client, db, settings):
    """
    Anonymous are not allowed and is redirect to login.
    """
    url = reverse("atoum:shopping-list-index")
    response = client.get(url, follow=True)
    assert response.redirect_chain == [
        ("{}?next={}".format(settings.LOGIN_URL, url), 302),
    ]
    assert response.status_code == 200


def test_index_empty(client, db):
    """
    Shopping index should just respond with an empty list.
    """
    user = UserFactory()
    client.force_login(user)

    url = reverse("atoum:shopping-list-index")
    response = client.get(url, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 200

    dom = html_pyquery(response)
    assert len(dom.find(".shoppinglist-index .shoppinglists .item")) == 0


@freeze_time("2012-10-15 10:00:00")
def test_index_filled(client, db, initial_catalog,  # noqa: F811
                      django_assert_num_queries):
    """
    Shopping index should list all Shopping objects.
    """
    user = UserFactory()
    client.force_login(user)

    url = reverse("atoum:shopping-list-index")

    # NOTE: Planning date are manually defined to avoid trouble in result ordering
    tomorrow = datetime.datetime(2012, 10, 16, 10, 0).replace(tzinfo=ZoneInfo("UTC"))
    yesterday = datetime.datetime(2012, 10, 14, 10, 0).replace(tzinfo=ZoneInfo("UTC"))

    ShoppingFactory(title="Fontessa", planning=yesterday)
    ShoppingFactory(title="Foo", planning=tomorrow)
    ShoppingFactory(title="Bar", done=True)

    with django_assert_num_queries(4):
        response = client.get(url, follow=True)

    assert response.redirect_chain == []
    assert response.status_code == 200

    dom = html_pyquery(response)
    titles = [
        v.text
        for v in dom.find(".shoppinglist-index .shoppinglists .item .title")
    ]
    assert titles == ["Foo", "Fontessa", "Bar"]


def test_detail_filled(client, db, initial_catalog,  # noqa: F811
                       django_assert_num_queries):
    """
    Shopping detail should list its related items.
    """
    user = UserFactory()
    client.force_login(user)

    shopping = ShoppingFactory(fill_products=[
        (initial_catalog.products["corn"], {"quantity": 1}),
        (initial_catalog.products["steack"], {"quantity": 1, "done": True}),
        (initial_catalog.products["tomatoe"], {"quantity": 42}),
    ])

    url = reverse("atoum:shopping-list-detail", kwargs={"pk": shopping.id})

    with django_assert_num_queries(5):
        response = client.get(url, follow=True)

    assert response.redirect_chain == []
    assert response.status_code == 200

    dom = html_pyquery(response)
    titles = [
        v.text
        for v in dom.find(".shopping-detail .shopping-items .item .title")
    ]
    assert titles == ["Corn", "Steack", "Tomatoe"]


def test_detail_controls(client, db, initial_catalog):  # noqa: F811
    """
    Check about controls in detail view according to Shopping and basket variations.
    """
    # shopping_title_selector = ".shopping-detail .shopping-items .item .title"
    shopping_controls_selector = ".shopping-detail .head .controls a"

    user = UserFactory()
    client.force_login(user)

    # Create various Shopping objects
    shopping_empty = ShoppingFactory()
    shopping_undone = ShoppingFactory(fill_products=[
        (initial_catalog.products["tomatoe"], {"quantity": 42}),
    ])
    shopping_done = ShoppingFactory(done=True, fill_products=[
        (initial_catalog.products["steack"], {"quantity": 1}),
    ])

    # Shortcut to get control link from a shopping detail response
    def get_controls(shopping):
        url = reverse("atoum:shopping-list-detail", kwargs={"pk": shopping.id})
        response = client.get(url)
        assert response.status_code == 200
        return html_pyquery(response)

    # Without any opened Shopping, an undone Shopping is elligible to be opened
    dom = get_controls(shopping_undone)
    assert dom.find(shopping_controls_selector).attr("href") == reverse(
        "atoum:shopping-list-open-selection",
        kwargs={"pk": shopping_undone.id}
    )

    # Without any opened Shopping, an undone Shopping is elligible to be opened even
    # if empty
    dom = get_controls(shopping_empty)
    assert dom.find(shopping_controls_selector).attr("href") == reverse(
        "atoum:shopping-list-open-selection",
        kwargs={"pk": shopping_empty.id}
    )

    # Even without any opened Shopping, a Shopping done is not elligible
    dom = get_controls(shopping_done)
    assert dom.find(shopping_controls_selector).attr("href") is None

    # Make undone Shopping opened in basket
    session = client.session
    session["atoum_shopping_inventory"] = shopping_undone.id
    session.save()

    # A Shopping already set in basket does not show controls
    dom = get_controls(shopping_undone)
    assert dom.find(shopping_controls_selector).attr("href") is None

    # A done Shopping is never elligible
    dom = get_controls(shopping_done)
    assert dom.find(shopping_controls_selector).attr("href") is None

    # Any undone Shopping that is not set in basket will show controls
    dom = get_controls(shopping_empty)
    assert dom.find(shopping_controls_selector).attr("href") == reverse(
        "atoum:shopping-list-open-selection",
        kwargs={"pk": shopping_empty.id}
    )
