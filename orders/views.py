from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, View, UpdateView, ListView
from django.core.urlresolvers import reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import Http404

from .models import Checkout
from .forms import UpdateCheckoutForm
from products.models import Product


# class CheckoutView(DetailView):
#     template_name = 'accounts/profile.html'
#     success_url = reverse_lazy('orders:checkout')
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


# add to cart form
class CheckoutView(View):
    template_name = 'orders/checkout.html'

    def post(self, request, id):
        id = self.kwargs['id']
        qs = Checkout.objects.filter(product_id=id)
        if qs.exists():
            messages.success(request, 'You can not add this product because its already added before!')
            return redirect('orders:checkout')
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
            return redirect('orders:checkout')


# all orders page that submitted
class OrdersView(ListView):
    template_name = 'orders/orders.html'
    queryset = ''

    def get_context_data(self, **kwargs):
        context = super(OrdersView, self).get_context_data(**kwargs)
        context['title'] = 'Orders'
        context['orders'] = Checkout.objects.filter(user=self.request.user, status='accepted')
        return context


# checkout page
class CheckoutOrderView(ListView):
    template_name = 'orders/checkout.html'
    queryset = ''

    def get_context_data(self, **kwargs):
        context = super(CheckoutOrderView, self).get_context_data(**kwargs)
        context['title'] = 'Cart'
        context['orders'] = Checkout.objects.filter(user=self.request.user, status='pending')
        return context


# update order page
class CheckoutUpdateView(UpdateView):
    form_class = UpdateCheckoutForm
    model = Checkout
    template_name = 'orders/update_order.html'
    success_url = reverse_lazy('orders:checkout')

    # def get_success_url(self):
    #     return reverse('orders:checkout')

    def get_context_data(self, **kwargs):
        context = super(CheckoutUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Update Order'
        return context


# delete order
class OrderDeleteView(View):
    template_name = 'orders/checkout.html'

    def post(self, request, id):
        username = self.request.user
        if username is None:
            raise Http404
        else:
            qs = Checkout.objects.filter(id=id)
            if qs.exists() and qs.count() == 1:
                order = qs.first()
                order.delete()
                return redirect('orders:checkout')
