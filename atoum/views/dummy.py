from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class DummyView(LoginRequiredMixin, TemplateView):
    """
    Temporary dummy view that show nothing. Used for get_absolute_url from models until
    their detail view has been done.
    """
    template_name = "atoum/dummy.html"
