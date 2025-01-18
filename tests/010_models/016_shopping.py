import datetime
from zoneinfo import ZoneInfo

from django.core.exceptions import ValidationError

import pytest
from freezegun import freeze_time

from atoum.models import Shopping, ShoppingItem
from atoum.factories import ProductFactory, ShoppingFactory


@freeze_time("2012-10-15 10:00:00")
def test_basic(db):
    """
    Basic model validation with required fields should not fail
    """
    tomorrow = datetime.datetime(2012, 10, 16, 10, 0).replace(tzinfo=ZoneInfo("UTC"))

    shopping = Shopping(title="Foo", planning=tomorrow)
    shopping.full_clean()
    shopping.save()

    assert Shopping.objects.filter(title="Foo").count() == 1
    assert shopping.title == "Foo"


def test_required_fields(db, settings):
    """
    Basic models validation with missing required fields should fail.

    Note: There is no required fields on Shopping model.
    """
    settings.LANGUAGE_CODE = "en"

    ProductFactory(title="Romaine")
    ProductFactory(title="Arugula")

    shopping = Shopping(title="Foo")
    shopping.full_clean()
    shopping.save()

    shopping_romaine = ShoppingItem()
    with pytest.raises(ValidationError) as excinfo:
        shopping_romaine.full_clean()

    assert excinfo.value.message_dict == {
        "shopping": ["This field cannot be null."],
        "product": ["This field cannot be null."],
        "quantity": ["This field cannot be null."],
    }


@freeze_time("2012-10-15 10:00:00")
def test_items(db):
    """
    Adding shopping items should work but respect unique constraints
    """
    romaine = ProductFactory(title="Romaine")
    arugula = ProductFactory(title="Arugula")

    shopping = Shopping(title="Foo")
    shopping.full_clean()
    shopping.save()

    shopping_romaine = ShoppingItem(shopping=shopping, product=romaine, quantity=1)
    shopping_romaine.full_clean()
    shopping_romaine.save()

    shopping_arugula = ShoppingItem(shopping=shopping, product=arugula, quantity=42)
    shopping_arugula.full_clean()
    shopping_arugula.save()

    assert list(arugula.shoppingitem_set.all()) == [shopping_arugula]
    assert list(romaine.shoppingitem_set.all()) == [shopping_romaine]
    assert list(ShoppingItem.objects.all()) == [shopping_arugula, shopping_romaine]
    assert list(shopping.products.all()) == [arugula, romaine]

    # It should not be possible to add the same product for the same shopping list
    shopping_arugula = ShoppingItem(shopping=shopping, product=arugula, quantity=42)
    with pytest.raises(ValidationError) as excinfo:
        shopping_arugula.full_clean()

    assert excinfo.value.message_dict == {
        "__all__": ["Shopping item with this Shopping and Product already exists."]
    }


def test_factory_creation(db):
    """
    Factory should correctly create a new object without any errors
    """
    # Default Shopping don't have any product
    shopping = ShoppingFactory()
    assert shopping.products.count() == 0

    # Shopping with a random product item
    shopping = ShoppingFactory(fill_products=True)
    assert shopping.products.count() == 1


def test_factory_items_creation(db):
    """
    Factory should allow to create explicit item relations.
    """
    romaine = ProductFactory(title="Romaine")
    arugula = ProductFactory(title="Arugula")

    # Shopping with a random product item
    shopping = ShoppingFactory(fill_products=[
        (romaine, {"quantity": 2}),
        (arugula, {"quantity": 42}),
    ])
    assert shopping.products.count() == 2

    items = ShoppingItem.objects.all().values_list("product__title", flat=True)
    assert list(items) == [arugula.title, romaine.title]
    assert list(shopping.products.all()) == [arugula, romaine]
