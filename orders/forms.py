from django import forms
from django.contrib.auth import get_user_model
from .models import Checkout
from products.models import Product


User = get_user_model()


class UpdateCheckoutForm(forms.ModelForm):
    product_id = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = Checkout
        fields = [
            'product_id',
            'quantity',
        ]

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        qs = self.cleaned_data['product_id']
        available = Product.objects.filter(id=qs).first().quantity
        if quantity > available:
            raise forms.ValidationError('Quantity more than the available quantity = {}!'.format(available))
        if quantity == 0:
            raise forms.ValidationError('Quantity can not be less than 1')
        return quantity
