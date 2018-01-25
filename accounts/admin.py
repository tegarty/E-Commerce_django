from django.contrib import admin

from .models import Account, Gender

admin.site.register(Gender)
admin.site.register(Account)
