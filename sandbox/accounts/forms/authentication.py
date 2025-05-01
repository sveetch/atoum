from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm

from ..form_helpers import AuthenticationFormHelper


class AuthenticationForm(BaseAuthenticationForm):
    """
    Form to authenticate user.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = AuthenticationFormHelper()
