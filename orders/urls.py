from django.conf.urls import url

from .views import (
    CheckoutView,
    CheckoutUpdateView,
    OrderDeleteView,
    CheckoutOrderView,
    OrdersView,
    )

urlpatterns = [
    url(r'^order/(?P<id>\d+)/$', CheckoutView.as_view(), name='order'),
    url(r'^order/(?P<pk>\d+)/update/$', CheckoutUpdateView.as_view(), name='update'),
    url(r'^order/(?P<id>\d+)/delete/$', OrderDeleteView.as_view(), name='delete'),
    url(r'^cart/$', CheckoutOrderView.as_view(), name='checkout'),
    url(r'^$', OrdersView.as_view(), name='orders'),
]
