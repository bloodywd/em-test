from django.http import HttpResponse
from django.views.generic import ListView
from em_project.orders.models import Order


class OrderIndexView(ListView):
    template_name = 'orders/index.html'
    model = Order
