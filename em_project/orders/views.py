from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView
from rest_framework import viewsets

from em_project.orders.filters import OrderFilter
from em_project.orders.forms import OrderForm, OrderDeleteForm, \
    OrderUpdateForm, OrderItemForm
from em_project.orders.models import Order, OrderItem
from django.contrib import messages

from em_project.orders.serializers import OrderSerializer


class OrderIndexView(FilterView):
    model = Order
    filterset_class = OrderFilter
    template_name = 'orders/orders.html'
    context_object_name = 'order_list'
    paginate_by = 20
    extra_context = {'title': "Orders"}


class OrderCreateView(SuccessMessageMixin, CreateView):
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy("orders")
    extra_context = {'title': "Create order", 'button_name': 'Create'}
    success_message = "Order was created successfully"

    def form_valid(self, form):
        self.object = form.save()
        return redirect(
            reverse('edit_order_items', kwargs={'pk': self.object.pk}))


class OrderDeleteView(View):
    def get(self, request):
        form = OrderDeleteForm(request.GET or None)
        if form.is_valid():
            order_id = form.cleaned_data.get('order_id')
            if order_id and Order.objects.filter(id=order_id).exists():
                return redirect(
                    reverse("delete_order_by_id", args=(order_id,)))
            else:
                form.add_error('order_id',
                               'Order with this ID does not exist.')
        return render(request, 'orders/delete_order.html', {
            'form': form,
            'title': 'Delete Order',
            'button_name': 'Delete'
        })


class DeleteOrderByIDView(SuccessMessageMixin, DeleteView):
    model = Order
    template_name = 'orders/delete_order_by_id.html'
    success_url = reverse_lazy("orders")
    extra_context = {'title': "Delete order"}
    success_message = "Order was deleted successfully"


class OrderView(DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'orders/order.html'
    extra_context = {'title': "View order"}

    def get_queryset(self):
        return Order.objects.prefetch_related('items')


class OrderEditStatusView(SuccessMessageMixin, UpdateView):
    model = Order
    form_class = OrderUpdateForm
    context_object_name = 'order'
    success_url = reverse_lazy("orders")
    template_name = 'orders/order_form.html'
    success_message = "Order was updated successfully"
    extra_context = {
        'title': f'{"Update order"}',
        'button_name': 'Update'
    }


class OrderItemsEditView(View):
    def get(self, request, pk):
        order_item_form = OrderItemForm()
        order_items = OrderItem.objects.filter(order_id=pk).all()
        return render(request, 'orders/edit_order_items.html', {
            'form': order_item_form,
            'order_items': order_items,
            'title': f'Edit items of order {pk}',
            'button_name': 'Add item'
        })

    def post(self, request, pk):
        order = Order.objects.filter(id=pk).first()

        if 'delete_item' in request.POST:
            order_item_form = OrderItemForm()
            item_id = request.POST.get('delete_item')
            try:
                order_item = OrderItem.objects.get(id=item_id, order_id=pk)
                order_item.delete()
                messages.success(request, 'Item was deleted successfully')
            except OrderItem.DoesNotExist:
                messages.error(request, 'Item not found')
        else:
            order_item_form = OrderItemForm(request.POST)
            if order_item_form.is_valid():
                try:
                    order_item = order_item_form.save(commit=False)
                    order_item.order = order
                    order_item.save()
                    messages.success(request, 'Item was added successfully')
                except Exception as e:
                    messages.error(request,
                                   f'Error while saving item: {str(e)}')
        order_items = OrderItem.objects.filter(order_id=pk).all()

        order.update_total_price()
        order.save()
        return render(request, 'orders/edit_order_items.html', {
            'form': order_item_form,
            'order_items': order_items,
            'title': f'Edit items of order {pk}',
            'button_name': 'Add item'
        })


class CalculateIncomeView(View):
    def get(self, request):
        orders = Order.objects.filter(status='paid').prefetch_related(
            'items')
        total_income = orders.aggregate(total_income=Sum('total_price'))[
                           'total_income'] or 0

        return render(request, 'orders/income.html', {
            'order_list': orders,
            'title': 'Paid orders',
            'button_name': 'Search',
            'total_income': total_income
        })


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
