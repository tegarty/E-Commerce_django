from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView, View, ListView, UpdateView
from django.http import Http404
from django.conf import settings
from django.contrib import messages

from .models import Checkout
from .forms import UpdateCheckoutForm
from products.models import Product


# class CheckoutView(DetailView):
#     template_name = 'accounts/profile.html'
#     success_url = '/accounts/profile/'
#     queryset = ''
#
#     def get_object(self, **kwargs):
#         id = self.kwargs['id']
#         product = get_object_or_404(Product, id=id, publish=True)
#         checkout = Checkout.objects.create(
#             user=self.request.user,
#             name=product.name,
#             price=product.price,
#             quantity=product.quantity,
#             discount=product.discount,
#         )
#         return get_object_or_404(Product, id=id, publish=True)
#
#     def get_context_data(self, **kwargs):
#         context = super(CheckoutView, self).get_context_data(**kwargs)
#         context['title'] = 'Profile'
#         context['orders'] = Checkout.objects.filter(user=self.request.user)
#         return context


class CheckoutView(View):
    template_name = 'accounts/profile.html'
    # success_url = settings.LOGIN_REDIRECT_URL

    def post(self, request, id):
        id = self.kwargs['id']
        qs = Checkout.objects.filter(product_id=id)
        if qs.exists():
            messages.success(request, 'You can not add this product because its already added before!')
            return redirect('accounts:profile')
        else:
            product = get_object_or_404(Product, id=id, publish=True)
            checkout = Checkout.objects.create(
                user=self.request.user,
                product_id=id,
                name=product.name,
                price=product.price,
                quantity=1,
                discount=product.discount,
            )
            messages.success(request, 'Successfully Added!')
            return redirect('accounts:profile')


class CheckoutUpdateView(DetailView):
    # form_class = UpdateCheckoutForm
    # model = Checkout
    template_name = 'accounts/update_profile.html'

    def get_object(self):
        username = self.request.user
        if username is None:
            raise Http404
        return get_object_or_404(Checkout, user=username)

    def get_context_data(self, **kwargs):
        context = super(CheckoutUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Update Orders'
        return context
