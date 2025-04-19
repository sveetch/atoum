from atoum.factories import ShoppingFactory, UserFactory
from atoum.context_processors import session_data_processor


def test_empty(client, db, rf):
    """
    When there is no opened shopping list there is nothing to render
    """
    rf.session = client.session
    context = session_data_processor(rf)

    assert context == {"opened_shoppinglist": None}


def test_opened_exists(client, db, rf):
    """
    When session have an opened shopping list ID that exists it should be resolved to
    a ShoppingListInventory dataclasse.
    """
    user = UserFactory()
    opened_shopping = ShoppingFactory()

    client.force_login(user)
    rf.user = user

    # Set a shopping list different than the one given in URL args
    session = client.session
    session["atoum_shopping_selection"] = opened_shopping.id
    session.save()

    rf.session = session
    context = session_data_processor(rf)

    assert "opened_shoppinglist" in context
    assert context["opened_shoppinglist"] is not None
    assert context["opened_shoppinglist"].obj.id == opened_shopping.id


def test_opened_dont_exists(client, db, rf):
    """
    When session have an opened shopping list ID that does not exist the processor
    should silently remove it from session without error and context won't have it.
    """
    # Set a shopping list different than the one given in URL args
    session = client.session
    session["atoum_shopping_selection"] = "520"
    session.save()

    rf.session = session
    context = session_data_processor(rf)

    assert context["opened_shoppinglist"] is None
