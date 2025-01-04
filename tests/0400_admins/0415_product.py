from atoum.factories import ProductFactory
from atoum.models import Product
from atoum.utils.tests import (
    get_admin_add_url, get_admin_change_url, get_admin_list_url,
)


def test_key_admin_ping_add(db, admin_client):
    """
    Product model admin add form view should not raise error on GET request.
    """
    url = get_admin_add_url(Product)
    response = admin_client.get(url, follow=True)

    assert response.redirect_chain == []
    assert response.status_code == 200


def test_key_admin_ping_list(db, admin_client):
    """
    Product model admin list view should not raise error on GET request.
    """
    url = get_admin_list_url(Product)
    response = admin_client.get(url, follow=True)

    assert response.redirect_chain == []
    assert response.status_code == 200


def test_key_admin_ping_detail(db, admin_client):
    """
    Product model admin detail view should not raise error on GET request.
    """
    obj = ProductFactory()

    url = get_admin_change_url(obj)
    response = admin_client.get(url, follow=True)

    assert response.redirect_chain == []
    assert response.status_code == 200
