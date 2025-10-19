from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.views.generic import FormView
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...models import Product
from ...forms import ProductMoveToAdminForm
from .mixins import AdminContext


class ProductActionMoveAdminView(AdminContext, FormView):
    """
    Admin view to move all selected products to another Category.

    This is intended to be used from admin action from Product admin.
    """
    model = Product
    template_name = "atoum/admin/product/move_to.html"
    http_method_names = ["get", "post", "head", "options", "trace"]
    paginate_by = None
    form_class = ProductMoveToAdminForm
    previous_urlquery = None
    title = _("Move product(s) to a category")

    def get_selected_objects(self, selection):
        """
        Parse given id items divided by character ``,``.

        All item must be a valid integer.

        Arguments:
            selection (string): A list of id divided by comma inside a string.

        Returns:
            list: List of object id. Will raise just a null value if any of id is not a
            valid integer.
        """
        try:
            selection = [
                int(item)
                for item in selection.split(",")
            ]
        except ValueError:
            return None

        return selection

    def get_objects(self, selection):
        """
        Return a queryset of retrieved object from given selection.

        Arguments:
            selection (list): A list of integers for object selection.
        """
        return self.model.objects.filter(
            id__in=selection
        ).order_by("title").select_related(
            *Product.HIERARCHY_SELECT_RELATED
        )

    def get_context_data(self, **kwargs):
        # Set the selection of objects in template context
        kwargs["selection"] = self.objects

        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["products"] = self.objects
        kwargs["admin_filters"] = self.previous_urlquery

        return kwargs

    def get_success_url(self):
        """
        Return URL to redirect in case of successful form submit.

        Returns:
            string: URL to redirect to, possibly extended with URL query from
            changelist origin.
        """
        url = reverse("admin:atoum_product_changelist")

        if not self.previous_urlquery:
            return url

        return url + "?" + self.previous_urlquery

    def form_valid(self, form):
        """
        Perform operation
        """
        payload = form.save()

        msg = _("{} object(s) assigned to category: {}")

        messages.add_message(self.request, messages.INFO, msg.format(*payload))
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        """
        Return HTML response with a form to choose a new category where to move
        the selection of objects.
        """
        # Consume selection argument so it is not passed to success redirection
        origin_querystring = request.GET.copy()
        origin_querystring.pop("selection")
        self.previous_urlquery = origin_querystring.urlencode()

        self.selection = self.get_selected_objects(
            self.request.GET.get("selection", "")
        )
        if not self.selection:
            return HttpResponseBadRequest()

        self.objects = self.get_objects(self.selection)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Receive submitted POST request to perform "moving" operation if valid.
        """
        self.selection = self.get_selected_objects(
            self.request.POST.get("selection", "")
        )
        if not self.selection:
            return HttpResponseBadRequest()

        # Form drop the origin url query from URL to include them in a hidden input
        self.previous_urlquery = self.request.POST.get("admin_filters", "")

        self.objects = self.get_objects(self.selection)

        return super().post(request, *args, **kwargs)
