from django.conf.urls import url

from .views import (
    ProductsListView,
    ProductDetailView,
    AllProductsListView,
    CategoryListView,
    )

urlpatterns = [
    url(r'^category/(?P<category>[a-zA-Z0-9].*)/$', CategoryListView.as_view(), name='category'),
    url(r'^all/$', AllProductsListView.as_view(), name='all'),
    url(r'^(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name='detail'),
    url(r'^$', ProductsListView.as_view(), name='list'),
]
