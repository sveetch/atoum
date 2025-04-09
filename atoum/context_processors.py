from .models import Shopping, ShoppingListInventory


def session_data_processor(request):
    """
    A template context processor to search for some references in session, resolve them
    and inject them in a template context.

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
