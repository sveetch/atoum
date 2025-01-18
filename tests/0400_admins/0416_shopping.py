import pytest

from atoum.factories import ShoppingFactory
from atoum.models import Shopping
from atoum.utils.tests import (
    get_admin_add_url, get_admin_change_url, get_admin_list_url,
)


def test_admin_ping_add(db, admin_client):
    """
    Shopping model admin add form view should not raise error on GET request.
    """
    url = get_admin_add_url(Shopping)
    response = admin_client.get(url, follow=True)

    assert response.redirect_chain == []
    assert response.status_code == 200


def test_admin_ping_list(db, admin_client):
    """
    Shopping model admin list view should not raise error on GET request.
    """
    url = get_admin_list_url(Shopping)
    response = admin_client.get(url, follow=True)

    assert response.redirect_chain == []
    assert response.status_code == 200


@pytest.mark.skip("No factory yet.")
def test_admin_ping_detail(db, admin_client):
    """
    Shopping model admin detail view should not raise error on GET request.
    """
    obj = ShoppingFactory()

    url = get_admin_change_url(obj)
    response = admin_client.get(url, follow=True)

    assert response.redirect_chain == []
    assert response.status_code == 200
