import pytest

from atoum.factories import ProductFactory, ShoppingFactory
from atoum.models import Shopping, ShoppingItem
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


def test_admin_ping_detail(db, admin_client):
    """
    Shopping model admin detail view should not raise error on GET request.
    """
    obj = ShoppingFactory()

    url = get_admin_change_url(obj)
    response = admin_client.get(url, follow=True)

    assert response.redirect_chain == []
    assert response.status_code == 200


@pytest.mark.parametrize("payload, expected", [
    # If all items are undone, the shoppinglist should be undone
    (
        {"romaine_done": False, "arugula_done": False},
        {"shopping_done": False, "romaine_done": False, "arugula_done": False},
    ),
    # If there is at least one undone item, the shoppinglist should be undone
    (
        {"romaine_done": True, "arugula_done": False},
        {"shopping_done": False, "romaine_done": True, "arugula_done": False},
    ),
    # If all items are done, the shoppinglist should be done
    (
        {"romaine_done": True, "arugula_done": True},
        {"shopping_done": True, "romaine_done": True, "arugula_done": True},
    ),
    # If shoppinglist is marked done, all items should be done too
    # TODO: We currently don't enforce this from admin
    # (
    #     {"shopping_done": True},
    #     {"shopping_done": True, "romaine_done": True, "arugula_done": True},
    # ),
])
def test_admin_detail_inlines(db, admin_client, payload, expected):
    """
    Shopping list 'done' state should depend from its items state.
    """
    # Products to shop
    romaine = ProductFactory(title="Romaine")
    arugula = ProductFactory(title="Arugula")

    # Build shopping list with some products
    shopping = ShoppingFactory(fill_products=[
        (romaine, {"quantity": 2, "done": True}),
        (arugula, {"quantity": 42, "done": False}),
    ])
    # Get the 'through relations' for their own data
    arugula_through = ShoppingItem.objects.get(shopping=shopping, product=arugula)
    romaine_through = ShoppingItem.objects.get(shopping=shopping, product=romaine)

    # Form payload data
    prefix = "shoppingitem_set-"
    data = {
        # Shopping object fields
        "title": shopping.title,
        "done": payload.get("shopping_done", shopping.done),
        "created_0": "02/01/2025",
        "created_1": "15:41:02",
        "planning_0": "02/01/2025",
        "planning_1": "15:41:02",
        # Management form infos
        prefix + "TOTAL_FORMS": 2,
        prefix + "INITIAL_FORMS": 2,
        prefix + "MIN_NUM_FORMS": 0,
        prefix + "MAX_NUM_FORMS": 1000,
        # Romaine item
        prefix + "0-id": romaine_through.id,
        prefix + "0-shopping": shopping.id,
        prefix + "0-product": romaine.id,
        prefix + "0-quantity": romaine_through.quantity,
        prefix + "0-done": payload.get("romaine_done", romaine_through.done),
        # Arugula item
        prefix + "1-id": arugula_through.id,
        prefix + "1-shopping": shopping.id,
        prefix + "1-product": arugula.id,
        prefix + "1-quantity": arugula_through.quantity,
        prefix + "1-done": payload.get("arugula_done", arugula_through.done),
    }

    # POST data to form
    url = get_admin_change_url(shopping)
    response = admin_client.post(url, data, follow=True)
    # This should returns to index list in case of success
    assert response.redirect_chain == [(get_admin_list_url(Shopping), 302)]
    assert response.status_code == 200

    # Ensure objects 'done state' is in expected value
    shopping.refresh_from_db()
    arugula_through.refresh_from_db()
    romaine_through.refresh_from_db()
    assert shopping.done is expected["shopping_done"]
    assert arugula_through.done is expected["arugula_done"]
    assert romaine_through.done is expected["romaine_done"]
