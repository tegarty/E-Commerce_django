from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.views.generic import CreateView, DetailView, UpdateView, View
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from django.urls import reverse_lazy

from .forms import RegisterForm, LoginForm, UpdateProfileForm
from .models import Account
from orders.models import Checkout


User = get_user_model()


def activate_user_view(request, code=None):
    if code:
        qs = Account.objects.filter(activation_key=code)
        if qs.exists() and qs.count() == 1:
            account = qs.first()
            if not account.activated:
                user = account.user
                user.is_active = True
                user.save()
                account.activated = True
                account.activation_key = None
                account.save()
                return redirect("accounts:login")
    return redirect("accounts:login")


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = settings.LOGIN_REDIRECT_URL

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        context['title'] = 'Register'
        return context


class UserLoginView(View):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class(None)
        context = {
                'form': form,
                'title': 'Login'
            }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('accounts:profile')
        context = {
            'form': form,
            'title': 'Login'
        }
        return render(request, self.template_name, context)


class UserLogoutView(View):
    template_name = 'accounts/login.html'

    def get(self, request):
        logout(request)
        return redirect('accounts:login')


class UserChangePasswordView(View):
    form_class = PasswordChangeForm
    template_name = 'accounts/change_password.html'

    def get(self, request):
        form = self.form_class(None)
        context = {
            'form': form,
            'title': 'Change Password'
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('accounts:profile')
        context = {
            'form': form,
            'title': 'Change Password'
        }
        return render(request, self.template_name, context)


class UserProfileView(DetailView):
    template_name = 'accounts/profile.html'

    def get_object(self):
        username = self.request.user
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username, is_active=True)

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['title'] = 'Profile'
        # context['orders'] = Checkout.objects.filter(user=self.request.user)
        return context


class ProfileUpdateView(UpdateView):
    form_class = UpdateProfileForm
    model = Account
    # fields = [
    #     'gender',
    #     'country',
    #     'image',
    #     'region',
    #     'address1',
    #     'address2',
    #     'phone_number1',
    #     'phone_number2',
    #     'comments',
    # ]
    template_name = 'accounts/update_profile.html'
    success_url = reverse_lazy('accounts:profile')
    # lookup_field = 'id'
    # lookup_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Update Profile'
        return context


class ProfileDeleteView(View):
    template_name = 'accounts/profile.html'

    def post(self, request):
        username = self.request.user
        if username is None:
            raise Http404
        else:
            qs = User.objects.filter(username=self.request.user)
            if qs.exists() and qs.count() == 1:
                account = qs.first()
                account.delete()
                return redirect('accounts:login')

# def delete_user(request):
#     qs = User.objects.filter(username=request.user)
#     if qs.exists() and qs.count() == 1:
#         account = qs.first()
#         print(account)
#         print(account.id)
#         account.delete()
#         return redirect('accounts:login')
