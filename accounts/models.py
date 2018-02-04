from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_delete
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
import os

from .utils import code_generator


User = settings.AUTH_USER_MODEL


class Gender(models.Model):
    sex = models.CharField(max_length=12)

    def __str__(self):
        return self.sex


class Account(models.Model):
    user = models.OneToOneField(User)
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(default='default.png', blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    address1 = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    phone_number1 = models.IntegerField(blank=True, null=True)
    phone_number2 = models.IntegerField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    activation_key = models.CharField(max_length=120, blank=True, null=True)
    activated = models.BooleanField(default=False)
    block_review = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('accounts:update', kwargs={'pk': self.id})

    def send_activation_email(self):
        if not self.activated:
            self.activation_key = code_generator()
            self.save()
            path = reverse('accounts:activate', kwargs={'code': self.activation_key})
            subject = 'Activate Account'
            from_email = settings.DEFAULT_FROM_EMAIL
            message = 'Activate your account here: {}'.format(path)
            recipient_list = [self.user.email]
            html_message = '<p>Activate your account here: {}</p>'.format(path)
            print(html_message)
            sent_mail = send_mail(
                subject,
                message,
                from_email,
                recipient_list,
                fail_silently=False,
                html_message=html_message)
            return sent_mail


def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        profile, is_created = Account.objects.get_or_create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
            username=instance.username,
            email=instance.email,
        )


def pre_delete_account_img(sender, instance, *args, **kwargs):
    if instance.image:
        if instance.image == 'default.png':
            pass
        else:
            if os.path.isfile(instance.image.path):
                os.remove(instance.image.path)


pre_delete.connect(pre_delete_account_img, sender=Account)
post_save.connect(post_save_user_receiver, sender=User)
