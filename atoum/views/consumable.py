from django.shortcuts import get_object_or_404
from django.views.generic import ListView


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
