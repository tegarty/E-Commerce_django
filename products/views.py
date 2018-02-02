from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


from .models import Product, Category
from reviews.models import Review


class AllProductsListView(ListView):
    queryset = Product.objects.all().order_by('-id')
    template_name = 'products/all_products.html'
    paginate_by = 20

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
    # queryset = Product.objects.all()
    queryset = ''
    template_name = 'products/product_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['title'] = 'Home'
        context['latest_products'] = Product.objects.all().order_by('-id')[:6]  # [start(offset):stop(limit):step]
        context['recommended'] = Product.objects.all().order_by('number_of_sales')[:3]
        context['recommended_2'] = Product.objects.all().order_by('number_of_sales')[3:6]
        context['categories'] = Category.objects.all().order_by('category')
        context['active_slider'] = Product.objects.filter(slider=True)[:1]
        context['non_active_slider_1'] = Product.objects.filter(slider=True)[1:2]
        context['non_active_slider_2'] = Product.objects.filter(slider=True)[2:3]
        return context

    def post(self, request):
        minimum = self.request.POST.get('minimum')
        maximum = self.request.POST.get('maximum')
        search = self.request.POST.get('search')
        if search == '':
            return redirect('products:list')
        if search:
            queryset = Product.objects.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(category__category__icontains=search)
            ).distinct().order_by('-id')
            context = {
                'products': queryset,
                'categories': Category.objects.all().order_by('category'),
                'title': 'Search',
            }
            return render(request, 'products/categories.html', context)
        if not minimum == '' and not maximum == '':
            queryset = Product.objects.filter(price__range=(minimum, maximum)).order_by('-id')
            context = {
                'products': queryset,
                'categories': Category.objects.all().order_by('category'),
                'title': 'Price Range',
            }
            return render(request, 'products/categories.html', context)
        else:
            return redirect('products:list')


class ProductDetailView(DetailView):
    template_name = 'products/product_detail.html'

    def get_object(self):
        slug = self.kwargs['slug']
        product = Product.objects.filter(slug=slug).first()
        product.number_of_views += 1
        product.save()
        return get_object_or_404(Product, slug=slug, publish=True)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['recommended'] = Product.objects.all().order_by('number_of_sales')[:3]
        context['categories'] = Category.objects.all().order_by('category')
        context['reviews'] = Review.objects.filter(product__slug=self.kwargs['slug']).order_by('-id')
        context['review'] = Review.objects.filter(product__slug=self.kwargs['slug']).order_by('-id')[:1].first()
        try:
            context['review_form'] = Review.objects.filter(product__slug=self.kwargs['slug'], user=self.request.user).order_by('-id')[:1].first()
        except:
            pass
        return context


class CategoryListView(ListView):
    queryset = ''
    template_name = 'products/categories.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['title'] = 'Category'
        context['categories'] = Category.objects.all().order_by('category')
        context['products'] = Product.objects.filter(category__category=self.kwargs['category']).order_by('-id')
        context['current_category'] = self.kwargs['category']
        return context
