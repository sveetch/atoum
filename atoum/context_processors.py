from .models import Shopping, ShoppingListInventory


def session_data_processor(request):
    """
    A template context processor to search for some references in session, resolve them
    and inject them in a template context.

    NOTE: Because a context processor is not aware of current context, it can not
    know if a variable as already been set and so some views like
    ``ShoppinglistManageProductView`` may perform the same query to get it from session.
    Also context processor are applied during response, not from
    ``View.get_context_data()`` so the view can not stand on the context processor.

    TODO: We may look instead for a View mixin to bring the var in context so it can
    be driven from view and avoid getting opened shopping list object twice. Still the
    context processor could be helpful for external usage in other apps from a project.

    TODO: Test coverage.

    Args:
        request (object): A Django Request object

    Returns:
        dict: Variables to append to the template context.
    """
    shopping_id = request.session.get("atoum_shopping_selection")
    inventory = None

    # If there is an opened shopping in user session
    if shopping_id:
        try:
            shopping_obj = Shopping.objects.filter(**{"pk": shopping_id}).get()
        except Shopping.DoesNotExist:
            # Purge session item if it does not exists anymore
            del request.session["atoum_shopping_selection"]
        else:
            inventory = ShoppingListInventory(obj=shopping_obj)

    return {
        "opened_shoppinglist": inventory,
    }
