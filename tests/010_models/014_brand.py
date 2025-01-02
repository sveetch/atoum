from django.core.exceptions import ValidationError

import pytest

from atoum.models import Brand
from atoum.factories import BrandFactory


def test_basic(db):
    """
    Basic model validation with required fields should not fail
    """
    brand = Brand(title="Foo", slug="foo")
    brand.full_clean()
    brand.save()

    url = "/brands/{}/".format(brand.slug)

    assert Brand.objects.filter(title="Foo").count() == 1
    assert "Foo" == brand.title
    assert url == brand.get_absolute_url()


def test_required_fields(db, settings):
    """
    Basic model validation with missing required fields should fail
    """
    settings.LANGUAGE_CODE = "en"

    brand = Brand()

    with pytest.raises(ValidationError) as excinfo:
        brand.full_clean()

    assert excinfo.value.message_dict == {
        "slug": ["This field cannot be blank."],
        "title": ["This field cannot be blank."],
    }


def test_uniqueness(db, settings):
    """
    Uniqueness constraint should be respected.
    """
    settings.LANGUAGE_CODE = "en"

    foo = Brand(title="Foo", slug="foo")
    foo.full_clean()
    foo.save()

    foobis = Brand(title="Foo", slug="foo")

    with pytest.raises(ValidationError) as excinfo:
        foobis.full_clean()

    assert excinfo.value.message_dict == {
        "slug": ["Brand with this Slug already exists."],
        "title": ["Brand with this Title already exists."],
    }


def test_factory_creation(db):
    """
    Factory should correctly create a new object without any errors
    """
    brand = BrandFactory(title="foo")
    assert brand.title == "foo"
    assert brand.cover is not None
    assert brand.cover.name.endswith(".png") is True
