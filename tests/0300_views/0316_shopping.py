import datetime
from zoneinfo import ZoneInfo

from django.urls import reverse

from freezegun import freeze_time

from atoum.utils.tests import html_pyquery
from atoum.factories import ShoppingFactory

from tests.initial import initial_catalog  # noqa: F401


def test_index_empty(client, db):
    """
    Shopping list index should just respond with an empty list.
    """
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
    Shopping list index should list all available Shopping objects.
    """
    url = reverse("atoum:shopping-list-index")

    # NOTE: Planning date are manually defined to avoid trouble in result ordering
    tomorrow = datetime.datetime(2012, 10, 16, 10, 0).replace(tzinfo=ZoneInfo("UTC"))
    yesterday = datetime.datetime(2012, 10, 14, 10, 0).replace(tzinfo=ZoneInfo("UTC"))

    ShoppingFactory(title="Fontessa", planning=yesterday)
    ShoppingFactory(title="Foo", planning=tomorrow)
    ShoppingFactory(title="Bar", done=True)

    # Only a single queryset to list objects
    with django_assert_num_queries(2):
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
    Shopping list detail should list its related items.
    """
    shopping = ShoppingFactory(fill_products=[
        (initial_catalog.products["corn"], {"quantity": 1}),
        (initial_catalog.products["steack"], {"quantity": 1, "done": True}),
        (initial_catalog.products["tomatoe"], {"quantity": 42}),
    ])

    url = reverse("atoum:shopping-list-detail", kwargs={"pk": shopping.id})

    # A queryset for the main object, another one to list its related objects and
    # another one for pagination
    with django_assert_num_queries(2):
        response = client.get(url, follow=True)

    assert response.redirect_chain == []
    assert response.status_code == 200

    dom = html_pyquery(response)
    titles = [
        v.text
        for v in dom.find(".shopping-detail .shopping-items .item .title")
    ]
    assert titles == ["Corn", "Steack", "Tomatoe"]
