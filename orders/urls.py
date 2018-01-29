from django.conf.urls import url

from .views import (
    CheckoutView,
    CheckoutUpdateView,
    )

urlpatterns = [
    url(r'^order/(?P<id>\d+)/$', CheckoutView.as_view(), name='order'),
    url(r'^order/update/$', CheckoutUpdateView.as_view(), name='update'),
]
