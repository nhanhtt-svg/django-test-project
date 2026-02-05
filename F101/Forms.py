# F101/forms.py
from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """Form tạo đơn hàng"""
    class Meta:
        model = Order
        fields = ['customer_name', 'quantity']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 100
            })
        }
        labels = {
            'customer_name': 'Your Name',
            'quantity': 'Quantity'
        }
