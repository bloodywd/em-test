from django import forms
from .models import Order


class TaskForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number', 'items', 'total_price', 'status']
