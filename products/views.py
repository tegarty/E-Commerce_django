from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Product


class AllProductsListView(ListView):
    queryset = Product.objects.all().order_by('-id')
    template_name = 'products/all_products.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(AllProductsListView, self).get_context_data(**kwargs)

        qs = Product.objects.all().order_by('-id')
        paginator = Paginator(qs, self.paginate_by)
        page_request = 'page'
        page = self.request.GET.get(page_request)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)
        context['objects'] = queryset
        context['page_request'] = page_request

        context['title'] = 'All Products'
        return context


class ProductsListView(ListView):
    queryset = Product.objects.all()
    template_name = 'products/product_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['title'] = 'Home'
        context['latest_products'] = Product.objects.all().order_by('-id')[:6]  # [start(offset):stop(limit):step]
        context['recommended'] = Product.objects.all().order_by('number_of_sales')[:3]
        context['recommended_2'] = Product.objects.all().order_by('number_of_sales')[3:6]
        return context


class ProductDetailView(DetailView):
    template_name = 'products/product_detail.html'

    def get_object(self):
        slug = self.kwargs['slug']
        return get_object_or_404(Product, slug=slug, publish=True)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['recommended'] = Product.objects.all().order_by('number_of_sales')[:3]
        return context
