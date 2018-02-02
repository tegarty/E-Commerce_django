from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, View, UpdateView, ListView, TemplateView
from django.core.urlresolvers import reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import Http404

from .models import Checkout
from .forms import UpdateCheckoutForm
from products.models import Product
from accounts.models import Account


from django.shortcuts import render_to_response
from django.template import RequestContext



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
        qs = Checkout.objects.filter(product_id=id, status='waiting')
        if qs.exists():
            messages.success(request, 'You can not add this product because its already added before!')
            return redirect('orders:checkout')
        else:
            product = get_object_or_404(Product, id=id, publish=True)
            checkout = Checkout.objects.create(
                user=self.request.user,
                product_id=id,
                name=product.name,
                slug=product.slug,
                price=product.price,
                quantity=1,
                discount=product.discount,
                image=product.image,
            )
            messages.success(request, 'Successfully Added!')
            return redirect('orders:checkout')


# all orders page that submitted
class OrdersView(ListView):
    template_name = 'orders/orders.html'
    queryset = ''

    def get_context_data(self, **kwargs):
        context = super(OrdersView, self).get_context_data(**kwargs)
        context['title'] = 'Pending Orders'
        if self.request.user.is_authenticated:
            context['orders'] = Checkout.objects.filter(user=self.request.user, status='pending')
        else:
            raise Http404
        return context


# all orders page that submitted & accepted
class AcceptedOrdersView(ListView):
    template_name = 'orders/orders.html'
    queryset = ''

    def get_context_data(self, **kwargs):
        context = super(AcceptedOrdersView, self).get_context_data(**kwargs)
        context['title'] = 'Accepted Orders'
        if self.request.user.is_authenticated:
            context['orders'] = Checkout.objects.filter(user=self.request.user, status='accepted')
        else:
            raise Http404
        return context


# all orders page that submitted & rejected
class RejectedOrdersView(ListView):
    template_name = 'orders/orders.html'
    queryset = ''

    def get_context_data(self, **kwargs):
        context = super(RejectedOrdersView, self).get_context_data(**kwargs)
        context['title'] = 'Rejected Orders'
        if self.request.user.is_authenticated:
            context['orders'] = Checkout.objects.filter(user=self.request.user, status='rejected')
        else:
            raise Http404
        return context


# checkout page
class CheckoutOrderView(ListView):
    template_name = 'orders/checkout.html'
    queryset = ''

    def get_context_data(self, **kwargs):
        context = super(CheckoutOrderView, self).get_context_data(**kwargs)
        context['title'] = 'Cart'
        if self.request.user.is_authenticated:
            qs = Checkout.objects.filter(user=self.request.user, status='waiting')
            context['orders'] = qs
            orders = qs
            total = 0
            for order in orders:
                total += order.price * order.quantity
            context['total'] = total
        else:
            raise Http404
        return context


# # update order page
# class CheckoutUpdateView(UpdateView):
#     form_class = UpdateCheckoutForm
#     model = Checkout
#     template_name = 'orders/update_order.html'
#     success_url = reverse_lazy('orders:checkout')
#
#     # def get_success_url(self):
#     #     return reverse('orders:checkout')
#
#     def get_context_data(self, **kwargs):
#         context = super(CheckoutUpdateView, self).get_context_data(**kwargs)
#         context['title'] = 'Update Order {}'.format(Checkout.objects.filter(id=self.kwargs['pk']).first().name)
#         return context


# update order page
class CheckoutUpdateView(View):
    template_name = 'orders/checkout.html'

    def post(self, request, pk):
        quantity = int(request.POST['quantity'])
        product_id = request.POST['product_id']
        available = Product.objects.filter(id=product_id).first()
        if quantity > available.quantity:
            messages.success(request, 'Quantity more than the available quantity : {} for product : {}'.format(available.quantity, available.name))
            return redirect('orders:checkout')
        if quantity == 0 or quantity < 0:
            messages.success(request, 'Quantity can not be less than 1 for product : {}'.format(available.name))
            return redirect('orders:checkout')
        qs = Checkout.objects.filter(id=pk, status='waiting')
        if qs.exists() and qs.count() == 1:
            product_quantity = qs.first()
            product_quantity.quantity = quantity
            product_quantity.save()
            messages.success(request, 'Successfully Added!')
            return redirect('orders:checkout')


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


# Buy orders
class BuyOrdersView(View):
    template_name = 'orders/orders.html'

    def post(self, request):
        username = self.request.user
        if username is None:
            raise Http404
        else:
            user_id = Account.objects.filter(user=username).first()
            account = Account.objects.filter(user=username)
            qs = Checkout.objects.filter(user=username, status='waiting')
            if account.exists():
                user = account.first()
                if user.gender is None \
                or user.country is None \
                or user.region is None \
                or user.address1 is None \
                or user.phone_number1 is None \
                or user.phone_number2 is None:
                    messages.success(request, 'add your information first to complete buy orders!')
                    return redirect('accounts:update', pk=user_id.id)
            if qs.exists():
                for order in qs:
                    order.status = 'pending'
                    order.save()
                    product = Product.objects.filter(id=order.product_id).first()
                    product.quantity -= order.quantity
                    product.number_of_sales += 1
                    product.save()
                return redirect('orders:thank')


class BuyThankView(TemplateView):
    template_name = "orders/thank.html"

    def get_context_data(self, **kwargs):
        context = super(BuyThankView, self).get_context_data(**kwargs)
        context['title'] = 'Thank You'
        return context






def handler404(request):
    response = render_to_response('404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response
