from django.contrib import admin

from .models import ContactUs


class ContactUsModelAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'username',
        'e_mail',
        'phone',
        'message',
        'seen',
    ]
    list_display_links = ['id']
    list_editable = ['e_mail', 'seen']
    list_filter = [
        'username',
        'e_mail',
        'phone',
        'seen',
    ]
    search_fields = ['username', 'e_mail', 'phone']
    list_per_page = 50

    class Meta:
        model = ContactUs


admin.site.register(ContactUs, ContactUsModelAdmin)
