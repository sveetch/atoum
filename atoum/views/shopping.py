from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseServerError
from django.views import View
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..models import Product, Shopping
from .mixins import AtoumBreadcrumMixin


class ShoppinglistIndexView(AtoumBreadcrumMixin, ListView):
    """
    List of Shopping lists
    """
    model = Shopping
    template_name = "atoum/shopping/index.html"
    paginate_by = settings.ATOUM_SHOPPINGLIST_PAGINATION
    crumb_title = _("Shopping lists")
    crumb_urlname = "atoum:shopping-list-index"

    def get_queryset(self):
        # Append 'done' field over the common ordering fields so the undone lists
        # have higher priority
        ordering = ["done"] + self.model.COMMON_ORDER_BY
        return self.model.objects.order_by(*ordering)

    @property
    def crumbs(self):
        return [
            (
                ShoppinglistIndexView.crumb_title,
                reverse(ShoppinglistIndexView.crumb_urlname)
            ),
        ]


class ShoppinglistDetailView(AtoumBreadcrumMixin, SingleObjectMixin, TemplateView):
    """
    Shopping list detail
    """
    model = Shopping
    template_name = "atoum/shopping/detail.html"
    context_object_name = "shopping_object"
    crumb_title = None  # No usage since title depends from object
    crumb_urlname = "atoum:shopping-list-detail"

    @property
    def crumbs(self):
        return [
            (
                ShoppinglistIndexView.crumb_title,
                reverse(ShoppinglistIndexView.crumb_urlname)
            ),
            (
                str(self.object),
                reverse(self.crumb_urlname, kwargs={
                    "pk": self.object.id,
                })
            ),
        ]

    def get_object(self):
        """
        Get the Shopping list object
        """
        object_id = self.kwargs.get("pk")

        try:
            obj = Shopping.objects.filter(**{"pk": object_id}).get()
        except Shopping.DoesNotExist:
            msg = _("No {} found matching the query")
            raise Http404(msg.format(self.model._meta.verbose_name))

        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        return super().get(request, *args, **kwargs)


class ShoppinglistToggleSelectionView(SingleObjectMixin, View):
    """
    View to open or close a Shopping list for product selection.

    TODO: Test coverage.
    """
    model = Shopping

    def get_object(self):
        """
        Get the Shopping list object
        """
        object_id = self.kwargs.get("pk")

        try:
            obj = self.model.objects.filter(**{"pk": object_id}).get()
        except self.model.DoesNotExist:
            msg = _("No {} found matching the query")
            raise Http404(msg.format(self.model._meta.verbose_name))

        return obj

    def get(self, request, *args, **kwargs):
        url = reverse("atoum:dashboard")

        # TODO: Ensure given url path is always safe
        if "next" in self.request.GET:
            url = self.request.GET.get("next")

        # If shopping id is given add it as opened in session
        if "pk" in self.kwargs:
            self.object = self.get_object()
            self.request.session["atoum_shopping_selection"] = self.object.id
        # Else assume we have to close any opened shopping from session
        else:
            del self.request.session["atoum_shopping_selection"]

        return HttpResponseRedirect(url)


class ShoppinglistManageProductView(SingleObjectMixin, View):
    """
    View to add or remove a product from a Shopping list.

    TODO: Test coverage.

    TODO:
        It should provide different rendering depending it is an addition, edition or
        deletion.

        * Deletion should just have the quantity + add button;
        * Addition should return the quantity + edit button + delete button;
        * Edition should return the quantity + edit button + delete button;

        This would replace the product controls.

        Then there should be a <template> element containg the <tr> row of product from
        list and should define hx-swap-oob="true" and proper target to update the
        shopping list.
    """
    model = Shopping
    operation_name = None

    def get_shopping_object(self):
        """
        Get the Shopping list object
        """
        object_id = self.kwargs.get("pk")

        try:
            obj = self.model.objects.filter(**{"pk": object_id}).get()
        except self.model.DoesNotExist:
            msg = _("No {} found matching the query")
            raise Http404(msg.format(self.model._meta.verbose_name))

        return obj

    def get_product_object(self):
        """
        Get the Product object
        """
        object_id = self.kwargs.get("product_id")

        try:
            obj = Product.objects.filter(**{"pk": object_id}).get()
        except Product.DoesNotExist:
            msg = _("No {} found matching the query")
            raise Http404(msg.format(Product._meta.verbose_name))

        return obj


    def get(self, request, *args, **kwargs):
        """
        GET verb is not supported.
        """
        return HttpResponseBadRequest()

    def delete(self, request, *args, **kwargs):
        """
        TODO: Should be only for deletion
        """
        self.shopping_object = self.get_shopping_object()
        self.product = self.get_product_object()

        self.operation_name = "delete"

        return HttpResponse("<p>Non mais ho</p>")

    def post(self, request, *args, **kwargs):
        """
        TODO:
        * Should be for addition or edition.
        * It's an edition if product is in shopping, else it is an addition.
        * Use swap-oob to edit the <tr> of product or just the new <tr> (at top of list)
          for addition
        """
        self.shopping_object = self.get_shopping_object()
        self.product = self.get_product_object()

        self.operation_name = "addition"
        self.operation_name = "edition"

        #return HttpResponseRedirect(url)
        return HttpResponse("<p>Non mais ho</p>")
