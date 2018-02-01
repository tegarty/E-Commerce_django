from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, View, UpdateView, ListView, CreateView, DeleteView
from django.core.urlresolvers import reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect

from .models import Review
from products.models import Product


class AddReviewView(View):
    template_name = 'products/product_detail.html'

    def post(self, request, id):
        review = request.POST.get('review')
        rate = request.POST.get('rate')
        product = get_object_or_404(Product, id=id, publish=True)
        if review == '' or rate is None:
            messages.success(request, 'You must write a valid product review!')
            return redirect('products:detail', slug=product.slug)
        qs = Review.objects.filter(user=self.request.user, product=product)
        if qs.exists():
            messages.success(request, 'You can not add this product review because you already added a review before!')
            return redirect('products:detail', slug=product.slug)
        else:
            review = Review.objects.create(
                user=self.request.user,
                product=product,
                review=review,
                rate=rate,
            )
            messages.success(request, 'Successfully added your product review!')
            return redirect('products:detail', slug=product.slug)


class DeleteReviewView(View):
    template_name = 'products/product_detail.html'

    def post(self, request, id):
        qs = Review.objects.filter(id=id)
        if qs.exists() and qs.count() == 1:
            review = qs.first()
            current_user = self.request.user
            username = review.user
            if current_user == username:
                review.delete()
                messages.success(request, 'deleted successfully!')
                return redirect('products:detail', slug=review.product.slug)
            else:
                messages.success(request, 'you can not delete this review because you don have the permission!')
                return redirect('products:detail', slug=review.product.slug)
