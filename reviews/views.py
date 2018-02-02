from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, View, UpdateView, ListView, CreateView, DeleteView, FormView
from django.core.urlresolvers import reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect

from .models import Review
from products.models import Product
from accounts.models import Account


class AddReviewView(View):
    template_name = 'products/product_detail.html'

    def post(self, request, id):
        review = request.POST.get('review')
        rate = request.POST.get('rate')
        product = get_object_or_404(Product, id=id, publish=True)
        if product.block_review is True:
            messages.success(request, 'This product is blocked for adding review products!')
            return redirect('products:detail', slug=product.slug)
        user = Account.objects.filter(user=self.request.user).first()
        if user.block_review is True:
            messages.success(request, 'You blocked from adding review products!')
            return redirect('products:detail', slug=product.slug)
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
            products = Review.objects.filter(product_id=id)
            summition_rate = 0
            products_length = 0
            for pro in products:
                summition_rate += pro.rate
                products_length += 1
            avg = summition_rate / products_length
            avg_rate = Product.objects.get(id=id)
            avg_rate.avg_rate = avg
            avg_rate.save()
            messages.success(request, 'Successfully added your product review!')
            return redirect('products:detail', slug=product.slug)


class UpdateReviewView(View):
    template_name = 'products/product_detail.html'

    def post(self, request, id):
        review = request.POST.get('review')
        rate = request.POST.get('rate')
        product = get_object_or_404(Product, id=id, publish=True)
        if product.block_review is True:
            messages.success(request, 'This product is blocked for editing review products!')
            return redirect('products:detail', slug=product.slug)
        user = Account.objects.filter(user=self.request.user).first()
        if user.block_review is True:
            messages.success(request, 'You blocked from editing review products!')
            return redirect('products:detail', slug=product.slug)
        if review == '' or rate is None:
            messages.success(request, 'You must write a valid product review!')
            return redirect('products:detail', slug=product.slug)
        qs = Review.objects.filter(user=self.request.user, product=product).first()
        qs.review = review
        qs.rate = rate
        qs.save()
        products = Review.objects.filter(product_id=id)
        summition_rate = 0
        products_length = 0
        for pro in products:
            summition_rate += pro.rate
            products_length += 1
        avg = summition_rate / products_length
        avg_rate = Product.objects.get(id=id)
        avg_rate.avg_rate = avg
        avg_rate.save()
        messages.success(request, 'Edited successfully!')
        return redirect('products:detail', slug=product.slug)


class DeleteReviewView(View):
    template_name = 'products/product_detail.html'

    def post(self, request, id):
        qs = Review.objects.filter(id=id)
        product_id = qs.first().product.id
        product = get_object_or_404(Product, id=product_id, publish=True)
        if product.block_review is True:
            messages.success(request, 'This product is blocked for deleting review products!')
            return redirect('products:detail', slug=product.slug)
        if qs.exists() and qs.count() == 1:
            review = qs.first()
            user = Account.objects.filter(user=self.request.user).first()
            if user.block_review is True:
                messages.success(request, 'You blocked from deleting review products!')
                return redirect('products:detail', slug=review.product.slug)
            current_user = self.request.user
            username = review.user
            if current_user == username:
                review.delete()
                products = Review.objects.filter(product_id=product_id)
                summition_rate = 0
                products_length = 0
                for pro in products:
                    summition_rate += pro.rate
                    products_length += 1
                try:
                    avg = summition_rate / products_length
                except ZeroDivisionError:
                    avg = 0
                avg_rate = Product.objects.get(id=product_id)
                avg_rate.avg_rate = avg
                avg_rate.save()
                messages.success(request, 'deleted successfully!')
                return redirect('products:detail', slug=review.product.slug)
            else:
                messages.success(request, 'you can not delete this review because you don have the permission!')
                return redirect('products:detail', slug=review.product.slug)
