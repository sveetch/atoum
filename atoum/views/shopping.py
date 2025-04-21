from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import RedirectURLMixin
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponseBadRequest
from django.views import View
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..models import Product, Shopping, ShoppingItem
from ..context_processors import session_data_processor
from .mixins import AtoumBreadcrumMixin


class ShoppinglistIndexView(AtoumBreadcrumMixin, LoginRequiredMixin, ListView):
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


class ShoppinglistDetailView(AtoumBreadcrumMixin, LoginRequiredMixin, SingleObjectMixin,
                             TemplateView):
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
        return get_object_or_404(self.model, pk=self.kwargs.get("pk"))

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        return super().get(request, *args, **kwargs)


class ShoppinglistToggleSelectionView(LoginRequiredMixin, RedirectURLMixin,
                                      SingleObjectMixin, View):
    """
    View to open or close a Shopping list for product selection.

    For opening it requires the shopping ID in "pk" argument from URL. For closing it
    does not require anything and just blindly purge the session variable.
    """
    model = Shopping
    raise_exception = True

    def get_object(self):
        """
        Get the Shopping list object
        """
        return get_object_or_404(self.model, pk=self.kwargs.get("pk"))

    def get(self, request, *args, **kwargs):
        self.next_page = reverse("atoum:dashboard")

        url = self.get_success_url()

        # If shopping id is given add it as opened in session
        if "pk" in self.kwargs:
            self.object = self.get_object()
            self.request.session["atoum_shopping_selection"] = self.object.id
        # Else assume we have to close any opened shopping from session
        else:
            del self.request.session["atoum_shopping_selection"]

        return HttpResponseRedirect(url)


class ShoppinglistManageProductView(LoginRequiredMixin, SingleObjectMixin,
                                    TemplateView):
    """
    View to add or remove a product from a Shopping list.

    This has been done for usage from htmx so it won't return a proper HTML page
    document.
    """
    model = Shopping
    template_name = "atoum/shopping/manage_opened_list.html"
    operation_name = None
    raise_exception = True

    def delete_shopping_item(self):
        """
        Remove the given product item from the Shopping list.

        Returns:
            dict: Return dict with some values (id and quantity) from deleted object.
        """
        obj = get_object_or_404(
            ShoppingItem,
            shopping=self.object,
            product=self.product
        )

        # Memorize useful data from object because template still use it
        memorized = {"id": obj.id, "quantity": obj.quantity}
        # Finally deletes the item
        obj.delete()
        self.operation_name = "deletion"

        return memorized

    def update_or_create_shopping_item(self, quantity):
        """
        Update or create the ShoppingItem object and possibly set its quantity if not
        null.

        Arguments:
            quantity (integer): The quantity to apply on object. It must be a greater
                or equal to 1 else it would not do nothing (except getting existing
                item).

        Returns:
            atoum.models.ShoppingItem: Return the existing or created object if
                quantity is greater or equal to 1. Else it returns the item object if
                it already exists or a null value if it does not exists yet.
        """
        try:
            obj = ShoppingItem.objects.filter(
                shopping=self.object,
                product=self.product
            ).get()
        except ShoppingItem.DoesNotExist:
            if quantity:
                obj = ShoppingItem(
                    shopping=self.object,
                    product=self.product,
                    quantity=quantity
                )
                obj.full_clean()
                obj.save()
                self.operation_name = "addition"
            else:
                obj = None
        else:
            if quantity:
                obj.quantity = quantity
                obj.full_clean()
                obj.save()
                self.operation_name = "edition"

        return obj

    def parse_quantity(self):
        """
        Parse given quantity from POST arguments.

        Returns:
            integer: Parsed quantity if it is a valid integer else returns a null
                value.
        """
        try:
            quantity = int(self.request.POST.get("quantity", 1))
        except ValueError:
            return None

        if not quantity or quantity < 1:
            quantity = 0

        return quantity

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "product": self.product,
            "shopping_item": self.shopping_item,
            "operation": self.operation_name,
        })

        return context

    def get(self, request, *args, **kwargs):
        """
        GET verb is not supported.
        """
        return HttpResponseBadRequest()

    def delete(self, request, *args, **kwargs):
        """
        DELETE verb allows for deletion of an existing product item from a shopping
        list.

        Response will only contains the HTML for product controls for a creation.
        """
        self.object = get_object_or_404(self.model, pk=self.kwargs.get("pk"))
        self.product = get_object_or_404(Product, pk=self.kwargs.get("product_id"))

        self.shopping_item = self.delete_shopping_item()

        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        """
        POST verb allows for creation or edition of a product item from a shopping list.

        If product is already an item of shopping list it is an edition and posted
        quantity will replace the previous value.

        Else if product is not in shopping list yet it is a creation and quantity will
        be set from posted value.

        Negative or null quantity is not allowed.

        Response will contains the HTML for product controls and possibly the new item
        row to append to the shopping list component in case of a creation.
        """
        self.object = get_object_or_404(self.model, pk=self.kwargs.get("pk"))
        self.product = get_object_or_404(Product, pk=self.kwargs.get("product_id"))

        quantity = self.parse_quantity()
        if quantity is None:
            return HttpResponseBadRequest()

        # Get opened shopping list from session
        inventory = session_data_processor(self.request).get(
            "opened_shoppinglist",
            None
        )

        if not inventory:
            msg = _("No opened shopping list")
            raise Http404(msg)
        elif inventory.obj.id != self.object.id:
            msg = _("Given Shopping is not the opened shopping list")
            raise Http404(msg)

        # Proceed to operation
        self.shopping_item = self.update_or_create_shopping_item(quantity)

        return self.render_to_response(self.get_context_data(**kwargs))
