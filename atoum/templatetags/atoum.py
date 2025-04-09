from collections.abc import Iterable

from django.conf import settings
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


@register.filter(is_safe=True)
def is_product_in_shoppinglist(value, arg):
    return value in arg


@register.simple_tag(takes_context=True)
def is_shopping_enabled(context):
    """
    A tag to find in user session if it have a Shopping list in selection
    mode or not.

    TODO: Test coverage.

    Exemple:
        Usage exemple is simple as: ::

            {% load atoum %}
            {% is_shopping_enabled %}

    Arguments:
        context (object): Either a ``django.template.Context`` or a dictionnary for
            context variable for template where the tag is included.

    Returns:
        boolean:
    """
    if context.get("opened_shoppinglist", None):
        return True

    return False


@register.simple_tag(takes_context=True)
def shopping_list_html(context, **kwargs):
    """
    Render HTML for a current opened Shopping list.

    TODO: Test coverage.

    Exemple:
        Basic usage: ::

            {% load atoum %}
            {% shopping_list_html [template="foo/bar.html"] %}


    Arguments:
        context (object): A ``django.template.RequestContext`` object.

    Returns:
        string: Rendered template tag fragment.

    """  # noqa: E501
    template_path = kwargs.get("template") or settings.ATOUM_SHOPPING_ASIDE_TEMPLATE

    return loader.get_template(template_path).render({
        "request": context.request,
        "LANGUAGES": context.get("LANGUAGES"),
        "LANGUAGE_CODE": context.get("LANGUAGE_CODE"),
        "debug": context.get("debug", False),
        "user": context.get("user", None),
        "opened_shoppinglist": context.get("opened_shoppinglist", None),
        "opened_shoppinglist_items": context.get("opened_shoppinglist_items", []),
        "opened_shoppinglist_itemids": context.get("opened_shoppinglist_itemids", []),
    })


@register.simple_tag(takes_context=True)
def shopping_product_control(context, product, **kwargs):
    """
    Render HTML of available controls for a product against an opened shopping list.

    Exemple:
        Basic usage: ::

            {% load atoum %}
            {% shopping_product_control PRODUCT [template="foo/bar.html"] %}

    Arguments:
        product (atoum.models.Product): Product object.
        context (object): Either a ``django.template.Context`` or a dictionnary for
            context variable for template where the tag is included. This is only used
            with an Article object, so it should be safe to be empty for a Category.

    Returns:
        string: Rendered template tag fragment.

    """  # noqa: E501
    template_path = (
        kwargs.get("template") or settings.ATOUM_SHOPPING_PRODUCT_CONTROLS_TEMPLATE
    )

    opened_shoppinglist = context.get("opened_shoppinglist", None)

    return loader.get_template(template_path).render({
        "request": context.request,
        "LANGUAGES": context.get("LANGUAGES"),
        "LANGUAGE_CODE": context.get("LANGUAGE_CODE"),
        "debug": context.get("debug", False),
        "user": context.get("user", None),
        "opened_shoppinglist": opened_shoppinglist,
        "is_product_selected": (
            opened_shoppinglist.is_product_selected(product)
            if opened_shoppinglist else False
        ),
        "product": product,
    })
