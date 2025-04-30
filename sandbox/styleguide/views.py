from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin

from py_css_styleguide.django.views import StyleguideViewMixin


class StyleguideIndexView(LoginRequiredMixin, StyleguideViewMixin):
    """
    Display styleguide from CSS manifest
    """

    template_name = "styleguide/index.html"
    manifest_css_filepath = settings.STYLEGUIDE_MANIFEST_PATH
    manifest_json_filepath = settings.STYLEGUIDE_DUMP_PATH
    save_dump = settings.STYLEGUIDE_SAVE_DUMP
    development_mode = settings.DEBUG
    raise_exception = True
