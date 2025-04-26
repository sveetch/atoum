from django.urls import reverse

import pytest

from atoum.factories import ShoppingFactory, UserFactory
from atoum.models import ShoppingItem
from atoum.utils.tests import html_pyquery

from tests.initial import initial_catalog  # noqa: F401


def test_anonymous(client, db, initial_catalog):  # noqa: F811
    """
    Anonymous can not have an opened shopping list and are not allowed to perform a
    request on management view.
    """
    shopping = ShoppingFactory()

    # Set opened shopping list (even that in practice it should not be possible)
    session = client.session
    session["atoum_shopping_selection"] = shopping.id
    session.save()

    # Post request
    url = reverse("atoum:shopping-list-product", kwargs={
        "pk": shopping.id,
        "product_id": initial_catalog.products["wing"].id,
    })
    response = client.post(url, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 403

    # Delete request
    url = reverse("atoum:shopping-list-product", kwargs={
        "pk": shopping.id,
        "product_id": initial_catalog.products["wing"].id,
    })
    response = client.delete(url, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 403


def test_no_opened_shoppinglist(client, db, initial_catalog):  # noqa: F811
    """
    If there is no opened shopping list in user session a POST request will receive a
    404 response.
    """
    user = UserFactory()
    client.force_login(user)

    shopping = ShoppingFactory()

    url = reverse("atoum:shopping-list-product", kwargs={
        "pk": shopping.id,
        "product_id": initial_catalog.products["wing"].id,
    })
    response = client.post(url, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 404


def test_shopping_different_shoppinglist(client, db, initial_catalog):  # noqa: F811
    """
    If request point to a shopping object that is not the opened shopping list, the view
    will return 404 response.
    """
    user = UserFactory()
    client.force_login(user)

    unopened_shopping = ShoppingFactory()
    opened_shopping = ShoppingFactory()

    # Set a shopping list different than the one given in URL args
    session = client.session
    session["atoum_shopping_selection"] = opened_shopping.id
    session.save()

    url = reverse("atoum:shopping-list-product", kwargs={
        "pk": unopened_shopping.id,
        "product_id": initial_catalog.products["wing"].id,
    })
    response = client.post(url, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 404


@pytest.mark.parametrize("qty_value, row, delete, qty_returned", [
    (3, 1, 1, 3),
])
def test_post_add(client, db, initial_catalog, qty_value, row, delete,  # noqa: F811
                  qty_returned):
    """
    View perform operation and respond to POST with a HTML including controls and
    possible row.
    """
    user = UserFactory()
    corn = initial_catalog.products["corn"]
    wing = initial_catalog.products["wing"]

    shopping = ShoppingFactory(fill_products=[(corn, {"quantity": 1})])

    client.force_login(user)

    # Make Shopping list opened in session
    session = client.session
    session["atoum_shopping_selection"] = shopping.id
    session.save()

    # Post request to add product item in list
    url = reverse("atoum:shopping-list-product", kwargs={
        "pk": shopping.id,
        "product_id": wing.id,
    })
    response = client.post(url, data={"quantity": qty_value}, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 200

    dom = html_pyquery(response)
    # HTML contains all controls
    assert len(dom.find("#id_shopping-product-{}_quantity".format(wing.id))) == 1
    assert len(dom.find("#btn_shopping-product-{}-post".format(wing.id))) == 1
    assert len(dom.find("#btn_shopping-product-{}-delete".format(wing.id))) == delete

    # Get the created shopping item
    wing_item = ShoppingItem.objects.filter(
        shopping=shopping,
        product=wing
    ).get()
    wing_item_cssid = "#shopping-list-{shopping}-item-{item}".format(
        shopping=shopping.id,
        item=wing_item.id,
    )
    # HTML contains the shopping item row to add/replace in shopping list
    assert len(dom.find(wing_item_cssid)) == row
    # Posted quantity value has been set as initial quantity
    if qty_returned is not None:
        saved_quantity = dom.find(wing_item_cssid + " .quantity").text()
        assert saved_quantity.strip() == str(qty_returned)


@pytest.mark.parametrize("qty_value", [0, -1])
def test_post_add_fail(client, db, initial_catalog, qty_value):  # noqa: F811
    """
    Invalid quantity will have an empty response
    """
    user = UserFactory()
    corn = initial_catalog.products["corn"]
    wing = initial_catalog.products["wing"]

    shopping = ShoppingFactory(fill_products=[(corn, {"quantity": 1})])

    client.force_login(user)

    # Make Shopping list opened in session
    session = client.session
    session["atoum_shopping_selection"] = shopping.id
    session.save()

    # Post request to add product item in list
    url = reverse("atoum:shopping-list-product", kwargs={
        "pk": shopping.id,
        "product_id": wing.id,
    })
    response = client.post(url, data={"quantity": qty_value}, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 200
    assert response.content.decode().strip() == ""


@pytest.mark.parametrize("qty_value, row, qty_returned", [
    (3, 1, 3),
])
def test_post_edit(client, db, initial_catalog, qty_value, row,  # noqa: F811
                   qty_returned):
    """
    View perform operation and respond to POST with a HTML including controls and
    possible row.
    """
    user = UserFactory()
    corn = initial_catalog.products["corn"]

    shopping = ShoppingFactory(fill_products=[(corn, {"quantity": 1})])

    client.force_login(user)

    # Make Shopping list opened in session
    session = client.session
    session["atoum_shopping_selection"] = shopping.id
    session.save()

    # Get the existing shopping item
    corn_item = ShoppingItem.objects.filter(
        shopping=shopping,
        product=corn
    ).get()
    corn_item_cssid = "#shopping-list-{shopping}-item-{item}".format(
        shopping=shopping.id,
        item=corn_item.id,
    )

    # Post request to edit product item in list
    url = reverse("atoum:shopping-list-product", kwargs={
        "pk": shopping.id,
        "product_id": corn.id,
    })
    response = client.post(url, data={"quantity": qty_value}, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 200

    dom = html_pyquery(response)
    # HTML contains all controls
    assert len(dom.find("#id_shopping-product-{}_quantity".format(corn.id))) == 1
    assert len(dom.find("#btn_shopping-product-{}-post".format(corn.id))) == 1
    assert len(dom.find("#btn_shopping-product-{}-delete".format(corn.id))) == 1
    # HTML contains the shopping item row to add/replace in shopping list
    assert len(dom.find(corn_item_cssid)) == row
    # Posted quantity value has been additionated to initial quantity
    if qty_returned is not None:
        saved_quantity = dom.find(corn_item_cssid + " .quantity").text()
        assert saved_quantity.strip() == str(qty_returned)


@pytest.mark.parametrize("qty_value", [0, -1])
def test_post_edit_fail(client, db, initial_catalog, qty_value):  # noqa: F811
    """
    Invalid quantity will have an empty response
    """
    user = UserFactory()
    corn = initial_catalog.products["corn"]

    shopping = ShoppingFactory(fill_products=[(corn, {"quantity": 1})])

    client.force_login(user)

    # Make Shopping list opened in session
    session = client.session
    session["atoum_shopping_selection"] = shopping.id
    session.save()

    # Get the existing shopping item
    corn_item = ShoppingItem.objects.filter(
        shopping=shopping,
        product=corn
    ).get()
    corn_item_cssid = "#shopping-list-{shopping}-item-{item}".format(
        shopping=shopping.id,
        item=corn_item.id,
    )

    # Post request to edit product item in list
    url = reverse("atoum:shopping-list-product", kwargs={
        "pk": shopping.id,
        "product_id": corn.id,
    })
    response = client.post(url, data={"quantity": qty_value}, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 200
    assert response.content.decode().strip() == ""


def test_post_delete(client, db, initial_catalog):  # noqa: F811
    """
    View perform operation and respond to POST with a HTML including controls.
    """
    user = UserFactory()
    corn = initial_catalog.products["corn"]
    wing = initial_catalog.products["wing"]

    shopping = ShoppingFactory(fill_products=[(corn, {"quantity": 1})])

    client.force_login(user)

    # Make Shopping list opened in session
    session = client.session
    session["atoum_shopping_selection"] = shopping.id
    session.save()

    # Get the existing shopping item
    corn_item = ShoppingItem.objects.filter(
        shopping=shopping,
        product=corn
    ).get()
    corn_item_cssid = "#shopping-list-{shopping}-item-{item}".format(
        shopping=shopping.id,
        item=corn_item.id,
    )

    # Post request to delete a product that is no in list lead to a 404 response
    url = reverse("atoum:shopping-list-product", kwargs={
        "pk": shopping.id,
        "product_id": wing.id,
    })
    response = client.delete(url, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 404

    # Post request to delete a product that is in list return an HTML response
    url = reverse("atoum:shopping-list-product", kwargs={
        "pk": shopping.id,
        "product_id": corn.id,
    })
    response = client.delete(url, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 200

    assert shopping.get_items().count() == 0

    dom = html_pyquery(response, rooted=True)
    # HTML contains all controls
    assert len(dom.find("#id_shopping-product-{}_quantity".format(corn.id))) == 1
    assert len(dom.find("#btn_shopping-product-{}-post".format(corn.id))) == 1
    assert len(dom.find("#btn_shopping-product-{}-delete".format(corn.id))) == 0

    # Check the item row is here and define a deletion swap to htmlx
    item_row = dom.find(corn_item_cssid)
    assert len(item_row) == 1
    assert item_row[0].get("hx-swap-oob") == "delete"


def test_patch_done(client, db, initial_catalog):  # noqa: F811
    """
    PATCH request should update the item field 'done' and update Shopping field 'done'
    also.

    NOTE: We do not make assertions (yet?) on HTML from response since it may be subject
    to many changes.
    """
    user = UserFactory()
    corn = initial_catalog.products["corn"]
    wing = initial_catalog.products["wing"]

    shopping = ShoppingFactory(fill_products=[
        (corn, {"quantity": 1, "done": False}),
        (wing, {"quantity": 1, "done": True}),
    ])
    assert shopping.done == False

    client.force_login(user)

    # Make Shopping list opened in session
    session = client.session
    session["atoum_shopping_selection"] = shopping.id
    session.save()

    # Get the existing shopping item
    corn_item = ShoppingItem.objects.filter(shopping=shopping, product=corn).get()
    wing_item = ShoppingItem.objects.filter(shopping=shopping, product=wing).get()
    corn_url = reverse("atoum:shopping-list-product", kwargs={
        "pk": shopping.id,
        "product_id": corn.id,
    })
    wing_url = reverse("atoum:shopping-list-product", kwargs={
        "pk": shopping.id,
        "product_id": wing.id,
    })
    corn_done_cssid = "#shopping-list-{shopping}-item-{item}-done".format(
        shopping=shopping.id,
        item=corn_item.id,
    )
    wing_done_cssid = "#shopping-list-{shopping}-item-{item}-done".format(
        shopping=shopping.id,
        item=wing_item.id,
    )

    # With every items done the shopping should be done also
    response = client.patch(corn_url, data="done=true", follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 200
    assert [(v.product.title, v.done) for v in shopping.get_items()] == [
        ("Corn", True),
        ("Wing", True)
    ]
    shopping.refresh_from_db()
    assert shopping.done == True
    dom = html_pyquery(response, rooted=True)
    item_row = dom.find(corn_done_cssid)
    assert len(item_row) == 1

    # If an item is turning undone the shopping turns undone also
    response = client.patch(wing_url, data="done=false", follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 200
    assert [(v.product.title, v.done) for v in shopping.get_items()] == [
        ("Corn", True),
        ("Wing", False)
    ]
    shopping.refresh_from_db()
    assert shopping.done == False
    dom = html_pyquery(response, rooted=True)
    item_row = dom.find(wing_done_cssid)
    assert len(item_row) == 1
