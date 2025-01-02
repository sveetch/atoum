from django.core.exceptions import ValidationError

import pytest

from atoum.models import Product
from atoum.factories import ProductFactory, CategoryFactory


def test_basic(db):
    """
    Basic model validation with required fields should not fail
    """
    category = CategoryFactory()

    product = Product(category=category, title="Foo", slug="foo")
    product.full_clean()
    product.save()

    url = "/products/{}/".format(product.slug)

    assert Product.objects.filter(title="Foo").count() == 1
    assert "Foo" == product.title
    assert url == product.get_absolute_url()


def test_required_fields(db, settings):
    """
    Basic model validation with missing required fields should fail
    """
    settings.LANGUAGE_CODE = "en"

    product = Product()

    with pytest.raises(ValidationError) as excinfo:
        product.full_clean()

    assert excinfo.value.message_dict == {
        "category": ["This field cannot be null."],
        "slug": ["This field cannot be blank."],
        "title": ["This field cannot be blank."],
    }


def test_uniqueness(db, settings):
    """
    Uniqueness constraint should be respected.
    """
    settings.LANGUAGE_CODE = "en"

    category = CategoryFactory(title="foo")

    foo = Product(category=category, title="Foo", slug="foo")
    foo.full_clean()
    foo.save()

    foobis = Product(category=category, title="Foo", slug="foo")

    with pytest.raises(ValidationError) as excinfo:
        foobis.full_clean()

    assert excinfo.value.message_dict == {
        "slug": ["Product with this Slug already exists."],
        "title": ["Product with this Title already exists."],
    }


def test_factory_creation(db):
    """
    Factory should correctly create a new object without any errors
    """
    product = ProductFactory(category__title="pika", title="foo")
    assert product.title == "foo"
    assert product.category.title == "pika"
    assert product.cover is not None
    assert product.cover.name.endswith(".png") is True
