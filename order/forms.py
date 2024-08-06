from django import forms 
from order.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['first_name','last_name','email','phone','city','address','state','pin_code']

