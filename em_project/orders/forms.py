from django import forms
from django.forms import inlineformset_factory

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


class OrderSearchForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('', 'Any'),
        *Order.STATUS_CHOICES,
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)
    class Meta:
        model = Order
        fields = ['table_number', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['table_number'].required = False


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', ]
