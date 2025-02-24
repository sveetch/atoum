from atoum.forms import ShoppingAdminForm
from atoum.utils.tests import flatten_form_errors


def test_empty(db, settings):
    """
    Empty form should not be valid because of required fields.
    """
    f = ShoppingAdminForm({})

    validation = f.is_valid()
    assert validation is False
    assert flatten_form_errors(f) == {
        "created": ["This field is required."],
        "planning": ["This field is required."],
    }
