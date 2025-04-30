from .models import Shopping


def session_data_processor(request):
    """
    A template context processor to discover for some references in session, resolve
    them and inject them in a template context.

    Arguments:
        request (object): A Django Request object.

    Returns:
        dict: Variables to append to the template context.
    """
    shopping_id = request.session.get("atoum_shopping_inventory")
    shopping_obj = None
    # Possible anonymous user with an ID in session (that should not occurs in practice)
    if (
        (not hasattr(request, "user") or not request.user.is_authenticated) and
        "atoum_shopping_inventory" in request.session
    ):
        del request.session["atoum_shopping_inventory"]
    # Stored ID in session for an authenticated user
    elif shopping_id:
        try:
            shopping_obj = Shopping.objects.filter(**{"pk": shopping_id}).get()
        except Shopping.DoesNotExist:
            # Purge session item if it does not exists anymore
            del request.session["atoum_shopping_inventory"]
            shopping_obj = None

    return {"shopping_inventory": shopping_obj}
