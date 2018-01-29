from django import forms
from django.contrib.auth import get_user_model
from .models import Checkout


User = get_user_model()


class UpdateCheckoutForm(forms.ModelForm):

    class Meta:
        model = Checkout
        fields = [
            # '',
        ]
