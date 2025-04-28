from collections.abc import Iterable

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.template import Library, loader

register = Library()


@register.simple_tag(name="querystring", takes_context=True)
def querystring(context, query_dict=None, **kwargs):
    """
    Add, remove, and change parameters of a ``QueryDict`` and return the result
    as a query string. If the ``query_dict`` argument is not provided, default
    to ``request.GET``.

    .. Note::
       This is a portage of the Django 5.1 new tag so we can benefit from it with
       Django<5.0 until we drop its support.

    For example::

        {% querystring foo=3 %}

    To remove a key::

        {% querystring foo=None %}

    To use with pagination::

        {% querystring page=page_obj.next_page_number %}

    A custom ``QueryDict`` can also be used::

        {% querystring my_query_dict foo=3 %}
    """
    if query_dict is None:
        query_dict = context.request.GET
    query_dict = query_dict.copy()
    for key, value in kwargs.items():
        if value is None:
            if key in query_dict:
                del query_dict[key]
        elif isinstance(value, Iterable) and not isinstance(value, str):
            query_dict.setlist(key, value)
        else:
            query_dict[key] = value
    if not query_dict:
        return ""
    query_string = query_dict.urlencode()
    return f"?{query_string}"


@register.simple_tag(takes_context=True)
def shopping_list_html(context, **kwargs):
    """
    Render HTML for an opened Shopping list.

    It does not expect any other argument than the optional template one. Everything
    else is discovered from template context (which should have been fullfilled from
    context processor with a ShoppingListInventory object).

    Exemple:
        Basic usage: ::

            {% load atoum %}
            {% shopping_list_html [template="foo/bar.html"] %}

    Arguments:
        context (object): A ``django.template.RequestContext`` object.

    Returns:
        string: Rendered template tag fragment with possible shopping list content.
        Render is only performed for authenticated user because anonymous are not
        allowed to manage a shopping list.

    """  # noqa: E501
    template_path = kwargs.get("template") or settings.ATOUM_SHOPPING_ASIDE_TEMPLATE
    user = context.get("user", None)

    if not user:
        return ""

    return loader.get_template(template_path).render({
        "request": context.request,
        "LANGUAGES": context.get("LANGUAGES"),
        "LANGUAGE_CODE": context.get("LANGUAGE_CODE"),
        "debug": context.get("debug", False),
        "user": context.get("user", None),
        "shopping_inventory": context.get("shopping_inventory", None),
    })


@register.simple_tag(takes_context=True)
def product_shopping_controls(context, product, **kwargs):
    """
    Render HTML of available controls for a product against an opened shopping list.

    This component is reserved to authenticated user. Rendered template has an isolated
    context.

    TODO:
        * Optimize the way to get 'shopping_item' for non opened inventory that will
          currently make a new query for each product this tag is called on;

    Exemple:
        Basic usage: ::

            {% load atoum %}
            {% shopping_product_control PRODUCT [shopping] [template="foo/bar.html"] %}

    Arguments:
        product (atoum.models.Product): Product object.
        context (object): Either a ``django.template.Context`` or a dictionnary for
            context variable for template where the tag is included. This is only used
            with an Article object, so it should be safe to be empty for a Category.

    Keyword Arguments:
        shopping (atoum.models.Shopping): Shopping object to use instead of inventory
            from session.

    Returns:
        string: Rendered template tag fragment.

    """  # noqa: E501
    user = getattr(context.request, "user", None)
    if not user or not user.is_authenticated:
        return ""

    shopping_object = kwargs.get("shopping")
    template_path = (
        kwargs.get("template") or settings.ATOUM_SHOPPING_PRODUCT_CONTROLS_TEMPLATE
    )

    shopping_inventory = context.get("shopping_inventory", None)

    tag_context = {
        "request": context.request,
        "LANGUAGES": context.get("LANGUAGES"),
        "LANGUAGE_CODE": context.get("LANGUAGE_CODE"),
        "debug": context.get("debug", False),
        "user": context.get("user", None),
        "current_shopping": None,
        "shopping_object": shopping_object,
        "shopping_inventory": shopping_inventory,
        "product": product,
        "is_product_shopped": False,
        "shopping_item": None,
    }

    if shopping_object and shopping_inventory and shopping_object.id == shopping_inventory.obj.id:
        tag_context["current_shopping"] = shopping_inventory.obj
        tag_context["is_product_shopped"] = shopping_inventory.is_product_shopped(product)
        tag_context["shopping_item"] = shopping_inventory.item_for_product(product)
    elif shopping_object:
        tag_context["current_shopping"] = shopping_object
        # TODO: We need a more efficient way to know if product is an item, the
        # following is making a query for each tag usage (currently it breaks some test
        # for their assertion of queryset count)
        try:
            tag_context["shopping_item"] = shopping_object.shoppingitem_set.get(product=product)
        except ObjectDoesNotExist:
            tag_context["shopping_item"] = None
        tag_context["is_product_shopped"] = (
            True if tag_context["shopping_item"] else False
        )
    elif shopping_inventory:
        tag_context["current_shopping"] = shopping_inventory.obj
        tag_context["is_product_shopped"] = shopping_inventory.is_product_shopped(product)
        tag_context["shopping_item"] = shopping_inventory.item_for_product(product)

    return loader.get_template(template_path).render(tag_context)
