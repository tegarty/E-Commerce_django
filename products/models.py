from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from .utils import create_slug


User = get_user_model()


class Category(models.Model):
    category = models.CharField(max_length=255)
    number_of_products = models.IntegerField(blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, null=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    quantity = models.IntegerField()
    discount = models.FloatField(blank=True, null=True)
    number_of_sales = models.IntegerField(blank=True, null=True)
    number_of_views = models.IntegerField(blank=True, null=True)
    avg_rate = models.FloatField(blank=True, null=True)
    description = models.TextField()
    image = models.ImageField()
    publish = models.BooleanField(default=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})


def pre_save_post_reciver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_reciver, sender=Product)
