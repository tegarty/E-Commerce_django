from django.contrib import admin

from .models import Review


class ReviewModelAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'product',
        'rate',
        'review',
    ]
    list_display_links = ['id']
    list_editable = ['rate', 'review']
    list_filter = [
        'user',
        'product',
        'rate',
    ]
    search_fields = ['user__username', 'product__name', 'rate']
    list_per_page = 50

    class Meta:
        model = Review


admin.site.register(Review, ReviewModelAdmin)
