from django.core.exceptions import ValidationError

import pytest

from atoum.models import Assortment
from atoum.factories import AssortmentFactory, ConsumableFactory


def test_basic(db):
    """
    Basic model validation with required fields should not fail
    """
    consumable = ConsumableFactory()

    assortment = Assortment(consumable=consumable, title="Foo", slug="foo")
    assortment.full_clean()
    assortment.save()

    url = "/consumables/{consumable}/{assortment}/".format(
        assortment=assortment.slug,
        consumable=assortment.consumable.slug,
    )

    assert Assortment.objects.filter(title="Foo").count() == 1
    assert "Foo" == assortment.title
    assert url == assortment.get_absolute_url()


def test_required_fields(db, settings):
    """
    Basic model validation with missing required fields should fail
    """
    settings.LANGUAGE_CODE = "en"

    assortment = Assortment()

    with pytest.raises(ValidationError) as excinfo:
        assortment.full_clean()

    assert excinfo.value.message_dict == {
        "consumable": ["This field cannot be null."],
        "slug": ["This field cannot be blank."],
        "title": ["This field cannot be blank."],
    }


def test_uniqueness(db, settings):
    """
    Uniqueness constraint should be respected.
    """
    settings.LANGUAGE_CODE = "en"

    consumable = ConsumableFactory(title="foo")

    foo = Assortment(consumable=consumable, title="Foo", slug="foo")
    foo.full_clean()
    foo.save()

    foobis = Assortment(consumable=consumable, title="Foo", slug="foo")

    with pytest.raises(ValidationError) as excinfo:
        foobis.full_clean()

    assert excinfo.value.message_dict == {
        "slug": ["Assortment with this Slug already exists."],
        "title": ["Assortment with this Title already exists."],
    }


def test_factory_creation(db):
    """
    Factory should correctly create a new object without any errors
    """
    assortment = AssortmentFactory(consumable__title="pika", title="foo")
    assert assortment.title == "foo"
    assert assortment.consumable.title == "pika"
