from django.conf.urls import url

from .views import (
    ProductsListView,
    ProductDetailView,
    AllProductsListView,
    )

urlpatterns = [
    url(r'^all/$', AllProductsListView.as_view(), name='all'),
    url(r'^$', ProductsListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name='detail'),
]
