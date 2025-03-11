from django import forms
from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number']


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['dish_name', 'price']


class OrderDeleteForm(forms.Form):
    order_id = forms.IntegerField(label='Order ID', min_value=1)


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', ]
