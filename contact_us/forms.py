from django import forms

from .models import ContactUs


class ContactUsForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={
            'placeholder': 'Username',
            'class': 'form-control',
        }))
    e_mail = forms.CharField(label='E-Mail', widget=forms.TextInput(
        attrs={
            'placeholder': 'E-Mail',
            'class': 'form-control',
        }))
    phone = forms.CharField(label='Phone Number', widget=forms.TextInput(
        attrs={
            'placeholder': 'Phone Number',
            'class': 'form-control',
        }))
    message = forms.Textarea()

    class Meta:
        model = ContactUs
        fields = [
            'username',
            'e_mail',
            'phone',
            'message',
        ]
