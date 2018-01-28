from django.contrib import admin

from .models import Category, Product


class ProductModelAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'id',
        'publish',
        'slider',
        'name',
        'price',
        'quantity',
        'discount',
        'number_of_sales',
        'number_of_views',
        'avg_rate',
        'category',
        'added',
        'updated'
    ]
    list_display_links = ['__str__']
    list_editable = ['name', 'price']
    list_filter = [
        'category',
        'publish',
        'slider',
        'price',
        'quantity',
        'discount',
        'number_of_sales',
        'number_of_views',
        'avg_rate'
    ]
    search_fields = ['name', 'description', 'price', 'discount']
    list_per_page = 50

    class Meta:
        model = Product


class CategoryModelAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'category',
        'number_of_products',
    ]
    list_display_links = ['id']
    list_editable = ['category', 'number_of_products']
    list_filter = [
        'category',
        'number_of_products',
    ]
    search_fields = ['category', 'number_of_products']
    list_per_page = 50

    class Meta:
        model = Category


admin.site.register(Category, CategoryModelAdmin)
admin.site.register(Product, ProductModelAdmin)
