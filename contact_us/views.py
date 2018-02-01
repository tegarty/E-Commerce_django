from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import ContactUsForm


class ContactUsView(CreateView):
    form_class = ContactUsForm
    template_name = 'contact_us/contact_us.html'
    success_url = reverse_lazy('products:list')

    def get_context_data(self, **kwargs):
        context = super(ContactUsView, self).get_context_data(**kwargs)
        context['title'] = 'Contact Us'
        return context
