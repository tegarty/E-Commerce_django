from django.db import models
from django.contrib.auth import get_user_model

from products.models import Product

User = get_user_model()


class Review(models.Model):
    RATE_CHOICES = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField(choices=RATE_CHOICES)
    review = models.TextField()
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{u} - {p} - {r}'.format(u=self.user, p=self.product, r=self.rate)
