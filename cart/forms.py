from django import forms

from store.models import Order


class order_form(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address','city','state','phone']




