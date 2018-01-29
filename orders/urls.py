from django.conf.urls import url

from .views import (
    CheckoutView,
    CheckoutUpdateView,
    CheckoutOrderView,
    OrdersView,
    )

urlpatterns = [
    url(r'^order/(?P<id>\d+)/$', CheckoutView.as_view(), name='order'),
    url(r'^order/(?P<pk>\d+)/update/$', CheckoutUpdateView.as_view(), name='update'),
    url(r'^cart/$', CheckoutOrderView.as_view(), name='checkout'),
    url(r'^$', OrdersView.as_view(), name='orders'),
]
