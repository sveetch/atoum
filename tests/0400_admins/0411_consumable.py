from atoum.factories import ConsumableFactory
from atoum.models import Consumable
from atoum.utils.tests import (
    get_admin_add_url, get_admin_change_url, get_admin_list_url,
)


def test_admin_ping_add(db, admin_client):
    """
    Consumable model admin add form view should not raise error on GET request.
    """
    url = get_admin_add_url(Consumable)
    response = admin_client.get(url, follow=True)

    assert response.redirect_chain == []
    assert response.status_code == 200


def test_admin_ping_list(db, admin_client):
    """
    Consumable model admin list view should not raise error on GET request.
    """
    url = get_admin_list_url(Consumable)
    response = admin_client.get(url, follow=True)

    assert response.redirect_chain == []
    assert response.status_code == 200


def test_admin_ping_detail(db, admin_client):
    """
    Consumable model admin detail view should not raise error on GET request.
    """
    obj = ConsumableFactory()

    url = get_admin_change_url(obj)
    response = admin_client.get(url, follow=True)

    assert response.redirect_chain == []
    assert response.status_code == 200
