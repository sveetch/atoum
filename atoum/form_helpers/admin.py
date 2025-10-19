from crispy_forms.layout import Div, Field, Fieldset, Layout

from .default import DefaultFormHelper


class AdminProductFormHelper(DefaultFormHelper):
    """
    Layout for "Product Move To" form.

    Try to reproduce the layout from Django admin.
    """
    DEFAULT_CSSID = "product_moveto_form"
    DEFAULT_CSSCLASSES = ""
    DEFAULT_ENABLETAG = False
    DEFAULT_INCLUDE_MEDIA = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def provide_layout(self, value=None, layout_args=None, layout_kwargs=None):
        self.layout = Layout(
            Fieldset(
                "",
                Div(
                    Div(
                        Field("destination", wrapper_class="flex-container required"),
                    ),
                    css_class="form-row",
                ),
                css_class="module aligned",
            ),
            "selection",
            "admin_filters",
        )
