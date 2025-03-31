import datetime
from zoneinfo import ZoneInfo

from django.core.exceptions import ValidationError

import pytest
from freezegun import freeze_time

from atoum.models import Shopping, ShoppingItem
from atoum.factories import (
    AssortmentFactory, ConsumableFactory, CategoryFactory, ProductFactory,
    ShoppingFactory
)


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
def test_add_items(db):
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

    shopping = ShoppingFactory(fill_products=[
        (romaine, {"quantity": 2}),
        (arugula, {"quantity": 42}),
    ])
    assert shopping.products.count() == 2

    items = ShoppingItem.objects.all().values_list("product__title", flat=True)
    assert list(items) == [arugula.title, romaine.title]
    assert list(shopping.products.all()) == [arugula, romaine]


@freeze_time("2012-10-15 10:00:00")
def test_get_items(db, django_assert_num_queries):
    """
    Method should return a queryset of all Shopping list items with their related
    product and in a single query.
    """
    romaine = ProductFactory(title="Romaine")
    arugula = ProductFactory(title="Arugula")

    shopping = ShoppingFactory(fill_products=[
        (romaine, {"quantity": 2}),
        (arugula, {"quantity": 42}),
    ])
    assert shopping.products.count() == 2

    with django_assert_num_queries(1):
        # Enforce usage of relevant attributes to ensure they don't hide further
        # querysets
        items_buffer = []
        for item in shopping.get_items():
            items_buffer.append((
                item.created,
                item.product.title,
                item.quantity,
                item.product.parenting_crumbs()
            ))


@freeze_time("2012-10-15 10:00:00")
def test_get_status(db, django_assert_num_queries):
    """
    Method should return correct data information about Shopping is open (no item done),
    ongoing (some items done) or done (all items are done).
    """
    consumable = ConsumableFactory(title="Consum")
    assortment = AssortmentFactory(consumable=consumable, title="Assort")
    category = CategoryFactory(assortment=assortment, title="Cat")
    romaine = ProductFactory(category=category, title="Romaine")
    arugula = ProductFactory(category=category, title="Arugula")
    beef = ProductFactory(category=category, title="Beef")
    egg = ProductFactory(category=category, title="Egg")
    tomatoe = ProductFactory(category=category, title="Tomatoe")

    openlist = ShoppingFactory(fill_products=[
        (romaine, {"quantity": 1}),
        (arugula, {"quantity": 1}),
        (beef, {"quantity": 1}),
        (egg, {"quantity": 1}),
        (tomatoe, {"quantity": 1}),
    ])
    assert openlist.done is False
    with django_assert_num_queries(1):
        assert openlist.get_status() == {"status": "open", "dones": 0, "opens": 5}

    ongoing = ShoppingFactory(fill_products=[
        (romaine, {"quantity": 1, "done": True}),
        (arugula, {"quantity": 1}),
        (beef, {"quantity": 1}),
        (egg, {"quantity": 1, "done": True}),
        (tomatoe, {"quantity": 1}),
    ])
    assert ongoing.done is False
    with django_assert_num_queries(1):
        assert ongoing.get_status() == {"status": "ongoing", "dones": 2, "opens": 3}

    done = ShoppingFactory(fill_products=[
        (romaine, {"quantity": 1, "done": True}),
        (arugula, {"quantity": 1, "done": True}),
        (beef, {"quantity": 1, "done": True}),
        (egg, {"quantity": 1, "done": True}),
        (tomatoe, {"quantity": 1, "done": True}),
    ])
    assert done.done is True
    with django_assert_num_queries(1):
        assert done.get_status() == {"status": "done", "dones": 5, "opens": 0}
