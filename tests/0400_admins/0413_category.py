from atoum.factories import CategoryFactory
from atoum.models import Category
from atoum.utils.tests import (
    get_admin_add_url, get_admin_change_url, get_admin_list_url,
)


def test_admin_ping_add(db, admin_client):
    """
    Category model admin add form view should not raise error on GET request.
    """
    url = get_admin_add_url(Category)
    response = admin_client.get(url, follow=True)

    assert response.redirect_chain == []
    assert response.status_code == 200


def test_admin_ping_list(db, admin_client):
    """
    Category model admin list view should not raise error on GET request.
    """
    url = get_admin_list_url(Category)
    response = admin_client.get(url, follow=True)

    assert response.redirect_chain == []
    assert response.status_code == 200


def test_admin_ping_detail(db, admin_client):
    """
    Category model admin detail view should not raise error on GET request.
    """
    obj = CategoryFactory()

    url = get_admin_change_url(obj)
    response = admin_client.get(url, follow=True)

    assert response.redirect_chain == []
    assert response.status_code == 200
