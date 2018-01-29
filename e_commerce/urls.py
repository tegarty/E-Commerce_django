from django.conf.urls import url, include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^products/', include('products.urls', namespace='products')),
    url(r'^orders/', include('orders.urls', namespace='orders')),
    # url(r'^$', include('products.urls')),
]# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
