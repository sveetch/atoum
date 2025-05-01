from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from crispy_forms.layout import Field, Layout
from crispy_forms.bootstrap import StrictButton

from atoum.form_helpers.default import DefaultFormHelper
from crispy_bootstrap5.bootstrap5 import FloatingField


class AuthenticationFormHelper(DefaultFormHelper):
    """
    Authentication form layout helper.
    """
    DEFAULT_ENABLETAG = False

    def provide_action(self, value=None):
        self.form_action = reverse("accounts:login")

    def provide_layout(self, value=None, layout_args=None, layout_kwargs=None):
        self.layout = Layout(
            FloatingField("username", wrapper_class=" "),
            FloatingField("password"),
            StrictButton("Login", type="submit", css_class="btn-primary w-100"),
        )
