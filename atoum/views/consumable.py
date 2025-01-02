from django.views.generic import ListView, TemplateView


from ..models import Consumable


class RecursiveTreeView(ListView):
    """
    Full recursive tree of Atoum objects (excepted Brand).
    """
    model = Consumable
    template_name = "atoum/recursivetree.html"
    paginate_by = None

    def get_queryset(self):
        q = self.model.objects.all()
        return q.order_by("title")


class DummyView(TemplateView):
    """
    Temporary dummy view that show nothing. Used for get_absolute_url from models until
    their detail view has been done.
    """
    template_name = "atoum/dummy.html"
