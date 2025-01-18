from django.core.exceptions import ValidationError

import pytest

from atoum.models import Category
from atoum.factories import CategoryFactory, AssortmentFactory


def test_basic(db):
    """
    Basic model validation with required fields should not fail
    """
    assortment = AssortmentFactory()

    category = Category(assortment=assortment, title="Foo", slug="foo")
    category.full_clean()
    category.save()

    url = "/consumables/{consumable}/{assortment}/{category}/".format(
        consumable=category.assortment.consumable.slug,
        assortment=category.assortment.slug,
        category=category.slug,
    )

    assert Category.objects.filter(title="Foo").count() == 1
    assert "Foo" == category.title
    assert url == category.get_absolute_url()


def test_required_fields(db, settings):
    """
    Basic model validation with missing required fields should fail
    """
    settings.LANGUAGE_CODE = "en"

    category = Category()

    with pytest.raises(ValidationError) as excinfo:
        category.full_clean()

    assert excinfo.value.message_dict == {
        "assortment": ["This field cannot be null."],
        "slug": ["This field cannot be blank."],
        "title": ["This field cannot be blank."],
    }


def test_uniqueness(db, settings):
    """
    Uniqueness constraint should be respected.
    """
    settings.LANGUAGE_CODE = "en"

    assortment = AssortmentFactory(title="foo")

    foo = Category(assortment=assortment, title="Foo", slug="foo")
    foo.full_clean()
    foo.save()

    foobis = Category(assortment=assortment, title="Foo", slug="foo")

    with pytest.raises(ValidationError) as excinfo:
        foobis.full_clean()

    assert excinfo.value.message_dict == {
        "__all__": [
            "Category with this Assortment and Title already exists.",
            "Category with this Assortment and Slug already exists.",
        ],
    }


def test_factory_creation(db):
    """
    Factory should correctly create a new object without any errors
    """
    category = CategoryFactory(assortment__title="pika", title="foo")
    assert category.title == "foo"
    assert category.assortment.title == "pika"
