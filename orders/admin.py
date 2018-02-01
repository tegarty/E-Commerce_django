from django.contrib import admin

from .models import Checkout


class CheckoutModelAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'status',
        'product_id',
        'name',
        'price',
        'quantity',
        'discount',
        'image',
    ]
    list_display_links = ['id']
    list_editable = ['status', 'name']
    list_filter = [
        'user',
        'status',
        'name',
        'price',
        'quantity',
        'discount',
    ]
    search_fields = ['user__username', 'name', 'price', 'discount']
    list_per_page = 50

    class Meta:
        model = Checkout


admin.site.register(Checkout, CheckoutModelAdmin)
