from django.conf.urls import url, include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from products.urls import ProductsListView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^products/', include('products.urls', namespace='products')),
    url(r'^orders/', include('orders.urls', namespace='orders')),
    url(r'^reviews/', include('reviews.urls', namespace='reviews')),
    url(r'^contact_us/', include('contact_us.urls', namespace='contact_us')),
    url(r'^$', ProductsListView.as_view(), name='main_home'),
]# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
