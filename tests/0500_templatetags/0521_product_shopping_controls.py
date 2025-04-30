from django.template import RequestContext

from atoum.utils.tests import html_pyquery
from atoum.factories import ProductFactory, ShoppingFactory, UserFactory
from atoum.templatetags.atoum import product_shopping_controls

from tests.initial import initial_catalog  # noqa: F401


# Shortcut for common CSS ID patterns
CSSID_DELETE = "#btn_shopping-product-{}-delete"
CSSID_FORM = "#form_shopping-product-{}"
CSSID_POST = "#btn_shopping-product-{}-post"
CSSID_QUANTITY = "#id_shopping-product-{}_quantity"


def test_empty(db, rf, settings):
    """
    When there is no opened shopping list there is nothing to render
    """
    render = product_shopping_controls(RequestContext(rf, {}), ProductFactory())

    assert render.strip() == ""


def test_anonymous(db, initial_catalog, rf, settings):  # noqa: F811
    """
    Render should be empty for an anonymous request.
    """
    corn = initial_catalog.products["corn"]
    shopping = ShoppingFactory()

    # Render for a product in shopping list
    context = RequestContext(
        rf,
        {
            "LANGUAGES": settings.LANGUAGES,
            "LANGUAGE_CODE": "en",
            "debug": False,
            "shopping_inventory": shopping,
        }
    )
    assert product_shopping_controls(context, corn) == ""


def test_in_inventory(client, db, initial_catalog, rf, settings):  # noqa: F811
    """
    When only inventory is provided and product is in inventory the controls should
    have all inputs and buttons for edition and delete.
    """
    user = UserFactory()
    client.force_login(user)
    rf.user = user

    corn = initial_catalog.products["corn"]
    shopping = ShoppingFactory(fill_products=[(corn, {"quantity": 42})])

    # Render for a product in shopping list
    context = RequestContext(
        rf,
        {
            "LANGUAGES": settings.LANGUAGES,
            "LANGUAGE_CODE": "en",
            "debug": False,
            "user": user,
            "shopping_inventory": shopping,
        }
    )
    render = product_shopping_controls(context, corn)
    dom = html_pyquery(render, rooted=True)
    assert len(dom.find(CSSID_FORM.format(corn.id))) == 1
    assert len(dom.find(CSSID_POST.format(corn.id))) == 1
    assert len(dom.find(CSSID_DELETE.format(corn.id))) == 1
    assert dom.find(CSSID_QUANTITY.format(corn.id)).attr("value") == "42"


def test_not_in_inventory(client, db, initial_catalog, rf, settings):  # noqa: F811
    """
    When only inventory is provided and product is not in inventory the controls should
    have inputs and button for addition.
    """
    user = UserFactory()
    client.force_login(user)
    rf.user = user

    wing = initial_catalog.products["wing"]
    corn = initial_catalog.products["corn"]
    shopping = ShoppingFactory(fill_products=[(corn, {"quantity": 42})])

    # Render for a product not in shopping list
    context = RequestContext(
        rf,
        {
            "LANGUAGES": settings.LANGUAGES,
            "LANGUAGE_CODE": "en",
            "debug": False,
            "user": user,
            "shopping_inventory": shopping,
        }
    )
    render = product_shopping_controls(context, wing)
    dom = html_pyquery(render, rooted=True)
    assert len(dom.find(CSSID_FORM.format(wing.id))) == 1
    assert len(dom.find(CSSID_POST.format(wing.id))) == 1
    assert len(dom.find(CSSID_DELETE.format(wing.id))) == 0
    assert dom.find(CSSID_QUANTITY.format(wing.id)).attr("value") == "1"


def test_in_shopping(client, db, initial_catalog, rf, settings):  # noqa: F811
    """
    When only shopping object is provided and product is in shopping object the
    controls should have all inputs and buttons for edition and delete
    """
    user = UserFactory()
    client.force_login(user)
    rf.user = user

    corn = initial_catalog.products["corn"]
    shopping = ShoppingFactory(fill_products=[(corn, {"quantity": 42})])

    # Render for a product in shopping list
    context = RequestContext(
        rf,
        {
            "LANGUAGES": settings.LANGUAGES,
            "LANGUAGE_CODE": "en",
            "debug": False,
            "user": user,
            "shopping_inventory": None,
        }
    )
    render = product_shopping_controls(context, corn, shopping=shopping)
    dom = html_pyquery(render, rooted=True)
    assert len(dom.find(CSSID_FORM.format(corn.id))) == 1
    assert len(dom.find(CSSID_POST.format(corn.id))) == 1
    assert len(dom.find(CSSID_DELETE.format(corn.id))) == 1
    assert dom.find(CSSID_QUANTITY.format(corn.id)).attr("value") == "42"


def test_not_in_shopping(client, db, initial_catalog, rf, settings):  # noqa: F811
    """
    When only shopping object is provided and product is in shopping object the controls
    should have all inputs and buttons for edition and delete
    """
    user = UserFactory()
    client.force_login(user)
    rf.user = user

    corn = initial_catalog.products["corn"]
    wing = initial_catalog.products["wing"]
    shopping = ShoppingFactory(fill_products=[(corn, {"quantity": 42})])

    # Render for a product in shopping list
    context = RequestContext(
        rf,
        {
            "LANGUAGES": settings.LANGUAGES,
            "LANGUAGE_CODE": "en",
            "debug": False,
            "user": user,
            "shopping_inventory": None,
        }
    )
    render = product_shopping_controls(context, wing, shopping=shopping)

    print("🎨 render:", render)

    dom = html_pyquery(render, rooted=True)
    assert len(dom.find(CSSID_FORM.format(wing.id))) == 1
    assert len(dom.find(CSSID_POST.format(wing.id))) == 1
    assert len(dom.find(CSSID_DELETE.format(wing.id))) == 0
    assert dom.find(CSSID_QUANTITY.format(wing.id)).attr("value") == "1"


def test_not_in_shopping_with_different(client, db, initial_catalog, rf,   # noqa: F811
                                        settings):
    """
    When different inventory and shopping object are provided and product is in
    inventory but not in shopping the controls should be for addition.

    It should be a case that we never integrate.
    """
    user = UserFactory()
    client.force_login(user)
    rf.user = user

    corn = initial_catalog.products["corn"]
    wing = initial_catalog.products["wing"]
    shopping_object = ShoppingFactory(fill_products=[(corn, {"quantity": 42})])
    shopping_inventory = ShoppingFactory(fill_products=[(wing, {"quantity": 51})])

    # Render for a product in shopping list
    context = RequestContext(
        rf,
        {
            "LANGUAGES": settings.LANGUAGES,
            "LANGUAGE_CODE": "en",
            "debug": False,
            "user": user,
            "shopping_inventory": shopping_inventory,
        }
    )
    render = product_shopping_controls(context, wing, shopping=shopping_object)
    dom = html_pyquery(render, rooted=True)
    assert len(dom.find(CSSID_FORM.format(wing.id))) == 1
    assert len(dom.find(CSSID_POST.format(wing.id))) == 1
    assert len(dom.find(CSSID_DELETE.format(wing.id))) == 0
    assert dom.find(CSSID_QUANTITY.format(wing.id)).attr("value") == "1"


def test_in_shopping_with_different(client, db, initial_catalog, rf,  # noqa: F811
                                    settings):
    """
    When different inventory and shopping object are provided and product is in shopping
    but not in inventory the controls should be for edition and deletion.
    """
    user = UserFactory()
    client.force_login(user)
    rf.user = user

    corn = initial_catalog.products["corn"]
    wing = initial_catalog.products["wing"]
    shopping_object = ShoppingFactory(fill_products=[(corn, {"quantity": 42})])
    shopping_inventory = ShoppingFactory(fill_products=[(wing, {"quantity": 51})])

    # Render for a product in shopping list
    context = RequestContext(
        rf,
        {
            "LANGUAGES": settings.LANGUAGES,
            "LANGUAGE_CODE": "en",
            "debug": False,
            "user": user,
            "shopping_inventory": shopping_inventory,
        }
    )
    render = product_shopping_controls(context, corn, shopping=shopping_object)
    dom = html_pyquery(render, rooted=True)
    assert len(dom.find(CSSID_FORM.format(corn.id))) == 1
    assert len(dom.find(CSSID_POST.format(corn.id))) == 1
    assert len(dom.find(CSSID_DELETE.format(corn.id))) == 1
    assert dom.find(CSSID_QUANTITY.format(corn.id)).attr("value") == "42"


def test_not_in_shopping_with_same(client, db, initial_catalog, rf,  # noqa: F811
                                   settings):
    """
    When same inventory and shopping object are provided and product is not in shopping
    the controls should be for addition.
    """
    user = UserFactory()
    client.force_login(user)
    rf.user = user

    corn = initial_catalog.products["corn"]
    wing = initial_catalog.products["wing"]
    shopping = ShoppingFactory(fill_products=[(corn, {"quantity": 42})])

    # Render for a product in shopping list
    context = RequestContext(
        rf,
        {
            "LANGUAGES": settings.LANGUAGES,
            "LANGUAGE_CODE": "en",
            "debug": False,
            "user": user,
            "shopping_inventory": shopping,
        }
    )
    render = product_shopping_controls(context, wing, shopping=shopping)
    dom = html_pyquery(render, rooted=True)
    assert len(dom.find(CSSID_FORM.format(wing.id))) == 1
    assert len(dom.find(CSSID_POST.format(wing.id))) == 1
    assert len(dom.find(CSSID_DELETE.format(wing.id))) == 0
    assert dom.find(CSSID_QUANTITY.format(wing.id)).attr("value") == "1"


def test_in_shopping_with_same(client, db, initial_catalog, rf,  # noqa: F811
                               settings):
    """
    When same inventory and shopping object are provided and product is in shopping the
    controls should be for edition and deletion.
    """
    user = UserFactory()
    client.force_login(user)
    rf.user = user

    corn = initial_catalog.products["corn"]
    shopping = ShoppingFactory(fill_products=[(corn, {"quantity": 42})])

    # Render for a product in shopping list
    context = RequestContext(
        rf,
        {
            "LANGUAGES": settings.LANGUAGES,
            "LANGUAGE_CODE": "en",
            "debug": False,
            "user": user,
            "shopping_inventory": shopping,
        }
    )
    render = product_shopping_controls(context, corn, shopping=shopping)
    dom = html_pyquery(render, rooted=True)
    assert len(dom.find(CSSID_FORM.format(corn.id))) == 1
    assert len(dom.find(CSSID_POST.format(corn.id))) == 1
    assert len(dom.find(CSSID_DELETE.format(corn.id))) == 1
    assert dom.find(CSSID_QUANTITY.format(corn.id)).attr("value") == "42"
