from django.db import models


class ContactUs(models.Model):
    username = models.CharField(max_length=255)
    e_mail = models.EmailField()
    phone = models.PositiveIntegerField()
    message = models.TextField()
    seen = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = 'Contact Us'
