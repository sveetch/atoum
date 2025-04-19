from django.template import RequestContext

from atoum.utils.tests import html_pyquery
from atoum.models import ShoppingListInventory
from atoum.factories import ShoppingFactory, UserFactory
from atoum.templatetags.atoum import shopping_list_html

from tests.initial import initial_catalog  # noqa: F401


def test_anonymous(client, db, rf, settings):
    """
    There is nothing to render for non authenticated users.
    """
    render = shopping_list_html(RequestContext(rf, {}))

    assert render.strip() == ""


def test_no_opened_shopping(client, db, rf, settings):
    """
    There is nothing to render if there is not opened shopping list.
    """
    user = UserFactory()

    client.force_login(user)
    rf.user = user

    context = RequestContext(
        rf,
        {
            "LANGUAGES": settings.LANGUAGES,
            "LANGUAGE_CODE": "en",
            "debug": False,
            "user": user,
            "opened_shoppinglist": None,
        }
    )
    render = shopping_list_html(context)

    assert render.strip() == ""


def test_render_opened_shopping(client, db, initial_catalog, rf,  # noqa: F811
                                settings):
    """
    Opened shopping list is rendered for authenticated user.
    """
    user = UserFactory()
    corn = initial_catalog.products["corn"]
    wing = initial_catalog.products["wing"]
    shopping = ShoppingFactory(fill_products=[
        (corn, {"quantity": 1}),
        (wing, {"quantity": 42}),
    ])

    client.force_login(user)
    rf.user = user

    context = RequestContext(
        rf,
        {
            "LANGUAGES": settings.LANGUAGES,
            "LANGUAGE_CODE": "en",
            "debug": False,
            "user": user,
            "opened_shoppinglist": ShoppingListInventory(obj=shopping),
        }
    )
    render = shopping_list_html(context)
    dom = html_pyquery(render, rooted=True)
    assert len(dom.find("#aside-shopping")) == 1

    title = dom.find("#aside-shopping > .head .title")
    assert len(title) == 1
    assert title.text() == shopping.title

    item_titles = [
        v.cssselect(".title")[0].text + ":" + v.cssselect(".quantity")[0].text
        for v in dom.find("#shopping-list-{} tbody tr".format(shopping.id))
    ]
    assert item_titles == ["Corn:1", "Wing:42"]
