from django.conf.urls import url

from .views import (
    CheckoutView,
    CheckoutUpdateView,
    OrderDeleteView,
    CheckoutOrderView,
    OrdersView,
    AcceptedOrdersView,
    RejectedOrdersView,
    BuyOrdersView,
    BuyThankView,
    )

urlpatterns = [
    url(r'^order/(?P<id>\d+)/$', CheckoutView.as_view(), name='order'),
    url(r'^order/(?P<pk>\d+)/update/$', CheckoutUpdateView.as_view(), name='update'),
    url(r'^order/(?P<id>\d+)/delete/$', OrderDeleteView.as_view(), name='delete'),
    url(r'^cart/$', CheckoutOrderView.as_view(), name='checkout'),
    url(r'^pending/$', OrdersView.as_view(), name='pending'),
    url(r'^rejected/$', RejectedOrdersView.as_view(), name='rejected'),
    url(r'^accepted/$', AcceptedOrdersView.as_view(), name='accepted'),
    url(r'^thank_you/$', BuyThankView.as_view(), name='thank'),
    url(r'^buy/$', BuyOrdersView.as_view(), name='buy'),
]
