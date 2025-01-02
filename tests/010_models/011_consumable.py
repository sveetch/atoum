from django.core.exceptions import ValidationError

import pytest

from atoum.models import Consumable
from atoum.factories import ConsumableFactory


def test_basic(db):
    """
    Basic model validation with required fields should not fail
    """
    consumable = Consumable(title="Foo", slug="foo")
    consumable.full_clean()
    consumable.save()

    url = "/consumables/{}/".format(consumable.slug)

    assert Consumable.objects.filter(title="Foo").count() == 1
    assert "Foo" == consumable.title
    assert url == consumable.get_absolute_url()


def test_required_fields(db, settings):
    """
    Basic model validation with missing required fields should fail
    """
    settings.LANGUAGE_CODE = "en"

    consumable = Consumable()

    with pytest.raises(ValidationError) as excinfo:
        consumable.full_clean()

    assert excinfo.value.message_dict == {
        "slug": ["This field cannot be blank."],
        "title": ["This field cannot be blank."],
    }


def test_uniqueness(db, settings):
    """
    Uniqueness constraint should be respected.
    """
    settings.LANGUAGE_CODE = "en"

    foo = Consumable(title="Foo", slug="foo")
    foo.full_clean()
    foo.save()

    foobis = Consumable(title="Foo", slug="foo")

    with pytest.raises(ValidationError) as excinfo:
        foobis.full_clean()

    assert excinfo.value.message_dict == {
        "slug": ["Consumable with this Slug already exists."],
        "title": ["Consumable with this Title already exists."],
    }


def test_factory_creation(db):
    """
    Factory should correctly create a new object without any errors
    """
    consumable = ConsumableFactory(title="foo")
    assert consumable.title == "foo"
