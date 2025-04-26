from django.urls import reverse

from atoum.factories import ShoppingFactory, UserFactory

from tests.initial import initial_catalog  # noqa: F401


def test_anonymous(client, db):
    """
    Anonymous is not allowed.
    """
    shopping = ShoppingFactory()

    url = reverse("atoum:shopping-list-close-selection")
    response = client.get(url, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 403

    url = reverse("atoum:shopping-list-open-selection", kwargs={"pk": shopping.id})
    response = client.get(url, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 403


def test_authenticated_close(client, db):
    """
    Closing opened shopping list will remove it from session, no matter it is valid
    value or not.
    """
    user = UserFactory()
    shopping = ShoppingFactory()
    client.force_login(user)

    # Make Shopping list opened in session
    session = client.session
    session["atoum_shopping_inventory"] = shopping.id
    session.save()

    consommables_url = reverse("atoum:consumable-index")
    url = reverse("atoum:shopping-list-close-selection")

    response = client.get(url, data={"next": consommables_url}, follow=True)
    assert response.redirect_chain == [(consommables_url, 302)]
    assert response.status_code == 200
    assert "atoum_shopping_inventory" not in client.session

    # With an invalid value does not raise error since it is just blindly purged
    session = client.session
    session["atoum_shopping_inventory"] = "wrong"
    session.save()

    response = client.get(url, data={"next": consommables_url}, follow=True)
    assert response.redirect_chain == [(consommables_url, 302)]
    assert response.status_code == 200
    assert "atoum_shopping_inventory" not in client.session


def test_authenticated_open_invalid(client, db):
    """
    Invalid Shopping ID will result on a 404.
    """
    user = UserFactory()
    client.force_login(user)

    url = reverse("atoum:shopping-list-open-selection", kwargs={"pk": 420})

    response = client.get(url, follow=True)
    assert response.redirect_chain == []
    assert response.status_code == 404
    assert "atoum_shopping_inventory" not in client.session


def test_authenticated_open_valid(client, db):
    """
    Valid Shopping ID should be set in session as the opened shopping list and possible
    redirection path followed.
    """
    user = UserFactory()
    shopping_1 = ShoppingFactory()
    shopping_2 = ShoppingFactory()

    dashboard_url = reverse("atoum:dashboard")
    consommables_url = reverse("atoum:consumable-index")

    client.force_login(user)

    # When session has no opened ID yet, also on default without given URL path it
    # safely redirects to the dashboard
    url = reverse("atoum:shopping-list-open-selection", kwargs={"pk": shopping_1.id})
    response = client.get(url, follow=True)
    assert response.redirect_chain == [(dashboard_url, 302)]
    assert response.status_code == 200
    assert "atoum_shopping_inventory" in client.session
    assert client.session["atoum_shopping_inventory"] == shopping_1.id

    # When session has already an opened ID it will be overwritten, also the given
    # URL path for redirection is followed
    url = reverse("atoum:shopping-list-open-selection", kwargs={"pk": shopping_2.id})
    response = client.get(url, data={"next": consommables_url}, follow=True)
    assert response.redirect_chain == [(consommables_url, 302)]
    assert response.status_code == 200
    assert "atoum_shopping_inventory" in client.session
    assert client.session["atoum_shopping_inventory"] == shopping_2.id
