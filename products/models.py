from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
import os

from .utils import create_slug


User = get_user_model()


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)
    number_of_products = models.IntegerField(default=0, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category

    def get_absolute_categories_url(self):
        return reverse('products:category', kwargs={'category': self.category})

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, null=True)
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    discount = models.FloatField(default=0, blank=True, null=True)
    number_of_sales = models.PositiveIntegerField(default=0, blank=True, null=True)
    number_of_views = models.PositiveIntegerField(default=0, blank=True, null=True)
    avg_rate = models.FloatField(default=0, blank=True, null=True)
    description = models.TextField()
    image = models.ImageField()
    slider = models.BooleanField(default=False)
    publish = models.BooleanField(default=True)
    block_review = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})


def pre_save_post_reciver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        qs = Product.objects.filter(slug=instance)
        if qs.exists() and qs.count() == 1:
            product = qs.first()
            category = Category.objects.get(category=product.category)
            category.number_of_products += 1
            category.save()


def pre_delete_product_img(sender, instance, *args, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


pre_save.connect(pre_save_post_reciver, sender=Product)
post_save.connect(post_save_user_receiver, sender=Product)
pre_delete.connect(pre_delete_product_img, sender=Product)
