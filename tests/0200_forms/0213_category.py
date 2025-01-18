from django.urls import reverse
from django.utils import timezone

from atoum.factories import AssortmentFactory, CategoryFactory, ConsumableFactory
from atoum.forms import CategoryAdminForm
from atoum.models import Category
from atoum.utils.tests import flatten_form_errors, html_pyquery


def test_empty(db, settings):
    """
    Empty form should not be valid because of required fields.
    """
    f = CategoryAdminForm({})

    validation = f.is_valid()
    assert validation is False
    assert flatten_form_errors(f) == {
        "assortment": ["This field is required."],
        "created": ["This field is required."],
        "modified": ["This field is required."],
        "title": ["This field is required."],
        "slug": ["This field is required."]
    }


def test_valid(db, settings):
    """
    Form should save object if submitted values are valid.
    """
    vegetable = AssortmentFactory(title="Vegetable")

    f = CategoryAdminForm({
        "assortment": vegetable,
        "created": timezone.now(),
        "modified": timezone.now(),
        "title": "Foo",
        "slug": "foo",
    })

    validation = f.is_valid()
    assert validation is True

    instance = f.save()
    assert Category.objects.all().count() == 1

    category = Category.objects.get(pk=instance.id)
    assert category.title == "Foo"
    assert category.slug == "foo"


def test_invalid_uniqueness(db, settings):
    """
    Form should not allow to create category with identical title or slug for the
    same assortment.
    """
    vegetable = AssortmentFactory(title="Vegetable")
    winter = AssortmentFactory(title="Winter")

    # Existing category
    CategoryFactory(assortment=vegetable, title="Foo", slug="foo")

    # With different assortment, title and slug can be reused
    f = CategoryAdminForm({
        "assortment": winter,
        "created": timezone.now(),
        "modified": timezone.now(),
        "title": "Foo",
        "slug": "foo",
    })
    validation = f.is_valid()
    assert validation is True

    # For the same assortment, title and slug can not be the same
    f = CategoryAdminForm({
        "assortment": vegetable,
        "created": timezone.now(),
        "modified": timezone.now(),
        "title": "Foo",
        "slug": "foo",
    })
    validation = f.is_valid()
    assert validation is False

    assert flatten_form_errors(f) == {
        "__all__": [
            "Category with this Assortment and Title already exists.",
            "Category with this Assortment and Slug already exists.",
        ],
    }


def test_assortment_field(db, settings):
    """
    Form field 'assortment' should be a select input from DAL widget attributes
    """
    food = ConsumableFactory(title="Food")
    vegetable = AssortmentFactory(consumable=food, title="Vegetable")
    AssortmentFactory(consumable=food, title="Fruits")

    # With empty form, DAL is enabled but there is only an empty option
    f = CategoryAdminForm()
    assortment_field = html_pyquery(f.as_p()).find("#id_assortment")
    assert assortment_field.attr("data-autocomplete-light-url") == reverse(
        "atoum:autocomplete-assortments"
    )
    assert assortment_field.attr("data-autocomplete-light-function") == "select2"
    assert [
        item.get("value")
        for item in assortment_field.find("option")
        if item.get("value")
    ] == []

    # With filled form, DAL is enabled but select input is filtered (from DAL widget)
    # to only contains the selected assortment
    f = CategoryAdminForm({
        "assortment": vegetable,
        "created": timezone.now(),
        "modified": timezone.now(),
        "title": "Foo",
        "slug": "foo",
    })
    assortment_field = html_pyquery(f.as_p()).find("#id_assortment")
    assert assortment_field.attr("data-autocomplete-light-url") == reverse(
        "atoum:autocomplete-assortments"
    )
    assert assortment_field.attr("data-autocomplete-light-function") == "select2"
    assert [
        (item.text, item.get("value"))
        for item in assortment_field.find("option")
        if item.get("value")
    ] == [("Food > Vegetable", str(vegetable.id))]
