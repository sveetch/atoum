from .models import Shopping, ShoppingListInventory


def session_data_processor(request):
    """
    A template context processor to discover for some references in session, resolve
    them and inject them in a template context.

    NOTE: Because a context processor is not aware of current context, it can not
    know if a variable as already been set and so some views like
    ``ShoppinglistManageProductView`` may perform the same query to get it from session.
    Also context processor are applied during response, not from
    ``View.get_context_data()`` so the view can not depend on the context processor
    result.

    Arguments:
        request (object): A Django Request object.

    Returns:
        dict: Variables to append to the template context.
    """
    shopping_id = request.session.get("atoum_shopping_selection")
    inventory = None
    # Possible anonymous user with an ID in session (that should not occurs in practice)
    if (
        (not hasattr(request, "user") or not request.user.is_authenticated) and
        "atoum_shopping_selection" in request.session
    ):
        del request.session["atoum_shopping_selection"]
    # Stored ID in session for an authenticated user
    elif shopping_id:
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
