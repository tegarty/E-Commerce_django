from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse


User = get_user_model()


class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, default='pending')
    product_id = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    discount = models.FloatField(default=0, blank=True, null=True)
    image = models.ImageField()
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})

    # def get_absolute_order_url(self):
    #     return reverse('orders:order', kwargs={'pk': self.id})
