from django.template import RequestContext

from atoum.utils.tests import html_pyquery
from atoum.models import ShoppingListInventory
from atoum.factories import ProductFactory, ShoppingFactory, UserFactory
from atoum.templatetags.atoum import shopping_product_controls

from tests.initial import initial_catalog  # noqa: F401


def test_empty(db, rf, settings):
    """
    When there is no opened shopping list there is nothing to render
    """
    render = shopping_product_controls(RequestContext(rf, {}), ProductFactory())

    assert render.strip() == ""


def test_product_controls(client, db, initial_catalog, rf, settings):  # noqa: F811
    """
    Tag should correctly render the HTML for the product controls.
    """
    user = UserFactory()
    corn = initial_catalog.products["corn"]
    wing = initial_catalog.products["wing"]
    shopping = ShoppingFactory(fill_products=[
        (corn, {"quantity": 1}),
    ])

    # Render for a product in shopping list
    context = RequestContext(
        rf,
        {
            "LANGUAGES": settings.LANGUAGES,
            "LANGUAGE_CODE": "en",
            "debug": False,
            "user": user,
            "shoppinglist_inventory": ShoppingListInventory(obj=shopping),
        }
    )
    render = shopping_product_controls(context, corn)
    dom = html_pyquery(render, rooted=True)
    assert len(dom.find("#form_shopping-product-{}".format(corn.id))) == 1
    assert len(dom.find("#id_shopping-product-{}_quantity".format(corn.id))) == 1
    assert len(dom.find("#btn_shopping-product-{}-post".format(corn.id))) == 1
    assert len(dom.find("#btn_shopping-product-{}-delete".format(corn.id))) == 1

    # Render for a product not in shopping list
    context = RequestContext(
        rf,
        {
            "LANGUAGES": settings.LANGUAGES,
            "LANGUAGE_CODE": "en",
            "debug": False,
            "user": user,
            "shoppinglist_inventory": ShoppingListInventory(obj=shopping),
        }
    )
    render = shopping_product_controls(context, wing)
    dom = html_pyquery(render, rooted=True)
    assert len(dom.find("#form_shopping-product-{}".format(wing.id))) == 1
    assert len(dom.find("#id_shopping-product-{}_quantity".format(wing.id))) == 1
    assert len(dom.find("#btn_shopping-product-{}-post".format(wing.id))) == 1
    assert len(dom.find("#btn_shopping-product-{}-delete".format(wing.id))) == 0
