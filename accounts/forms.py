from django import forms
from django.contrib.auth import get_user_model, authenticate
from .models import Account


User = get_user_model()


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(label='First name', widget=forms.TextInput(
        attrs={
            'placeholder': 'First name',
            'class': 'form-control',
        }))
    last_name = forms.CharField(label='Last name', widget=forms.TextInput(
        attrs={
            'placeholder': 'Last name',
            'class': 'form-control',
        }))
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={
            'placeholder': 'Username',
            'class': 'form-control',
        }))
    email = forms.CharField(label='E-mail', widget=forms.EmailInput(
        attrs={
            'placeholder': 'E-mail',
            'class': 'form-control',
        }))
    email_confirmation = forms.CharField(label='Confirm E-mail', widget=forms.EmailInput(
        attrs={
            'placeholder': 'Confirm E-mail',
            'class': 'form-control',
        }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password',
            'class': 'form-control',
        }))
    password_confirmation = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Confirm Password',
            'class': 'form-control',
        }))

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'email_confirmation',
            'password',
            'password_confirmation',
        ]

    def clean_email_confirmation(self):
        email = self.cleaned_data.get('email')
        email_confirmation = self.cleaned_data.get('email_confirmation')
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError('This email is already registered before!')
        if email and email_confirmation and email != email_confirmation:
            raise forms.ValidationError('Email dose not matched!')
        return email_confirmation

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError('Passwords dose not matched!')
        return password_confirmation

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = False
        if commit:
            user.save()
            user.account.send_activation_email()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={
            'placeholder': 'Username',
            'class': 'form-control',
        }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password',
            'class': 'form-control',
        }))

    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('User dose not exists!')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password!')
            if not user.is_active:
                raise forms.ValidationError('User is not active!')
        return super(LoginForm, self).clean(*args, **kwargs)


class UpdateProfileForm(forms.ModelForm):
    gender = forms.SelectMultiple()
    country = forms.CharField(label='Country', widget=forms.TextInput(
        attrs={
            'placeholder': 'Country',
            'class': 'form-control',
        }))
    region = forms.CharField(label='Region', widget=forms.TextInput(
        attrs={
            'placeholder': 'Region',
            'class': 'form-control',
        }))
    address1 = forms.CharField(label='Address 1', widget=forms.TextInput(
        attrs={
            'placeholder': 'Address 1',
            'class': 'form-control',
        }))
    address2 = forms.CharField(label='Address 2', required=False, widget=forms.TextInput(
        attrs={
            'placeholder': 'Address 2',
            'class': 'form-control',
        }))
    phone_number1 = forms.CharField(label='Phone Number 1', widget=forms.TextInput(
        attrs={
            'placeholder': 'Phone Number 1',
            'class': 'form-control',
        }))
    phone_number2 = forms.CharField(label='Phone Number 2', required=False, widget=forms.TextInput(
        attrs={
            'placeholder': 'Phone Number 2',
            'class': 'form-control',
        }))
    comments = forms.CharField(label='Comments', widget=forms.Textarea(
        attrs={
            'placeholder': 'Comments',
            'class': 'form-control',
        }))
    image = forms.ImageField(label='Image')

    class Meta:
        model = Account
        fields = [
            'gender',
            'country',
            'image',
            'region',
            'address1',
            'address2',
            'phone_number1',
            'phone_number2',
            'comments',
        ]

    def clean(self, *args, **kwargs):
        gender = self.cleaned_data.get('gender')
        country = self.cleaned_data.get('country')
        region = self.cleaned_data.get('region')
        address1 = self.cleaned_data.get('address1')
        phone_number1 = self.cleaned_data.get('phone_number1')
        phone_number2 = self.cleaned_data.get('phone_number2')
        if not gender:
            raise forms.ValidationError('Please select your gender!')
        if not country:
            raise forms.ValidationError('Please enter your country!')
        if not region:
            raise forms.ValidationError('Please enter your region!')
        if not address1:
            raise forms.ValidationError('Please enter your address1!')
        if not phone_number1:
            raise forms.ValidationError('Please enter your phone number1!')
        if not phone_number2:
            raise forms.ValidationError('Please enter your phone number2!')
        return super(UpdateProfileForm, self).clean(*args, **kwargs)
