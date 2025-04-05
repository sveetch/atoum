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
    if context.get("current_shoppinglist", None):
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
            {% translation_siblings_html [template="foo/bar.html"] %}


    Arguments:
        context (object): Either a ``django.template.Context`` or a dictionnary for
            context variable for template where the tag is included. This is only used
            with an Article object, so it should be safe to be empty for a Category.

    Returns:
        string: Rendered template tag fragment.

    """  # noqa: E501
    template_path = kwargs.get("template") or settings.ATOUM_SHOPPING_ASIDE_TEMPLATE

    render_context = {
        "request": context.request,
        "LANGUAGES": context["LANGUAGES"],
        "LANGUAGE_CODE": context["LANGUAGE_CODE"],
        "debug": context["debug"],
        "user": context["user"],
        "current_shoppinglist": context.get("current_shoppinglist", None),
    }

    return loader.get_template(template_path).render(render_context)
