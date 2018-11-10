from .forms import ContactForm
# from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.views import View

from django.http import (
    HttpResponseNotFound,
    HttpResponseRedirect,
    )
from django.shortcuts import render, reverse
from django.core.mail import EmailMessage


# Create your views here.

class SuccessView(View):
    template_name = 'contact/success.html'

    def get(self, request):
        if not request.session.get('form-submitted', False):
            return HttpResponseNotFound('<h1>Page not found</h1>')
        else:
            return render(request, self.template_name, {})


class ContactView(View):
    template_name = 'contact/contact.html'
    form_class = ContactForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            subject = 'Contact form submission from ' + form.cleaned_data['name']
            message = form.cleaned_data['message']
            reply_to = form.cleaned_data['reply_to']

            email = EmailMessage(
                subject=subject,
                body=message,
                to=['admin@localhost'],
                reply_to=[reply_to])
            email.send()

            request.session['form-submitted'] = True
            return HttpResponseRedirect(reverse('contact:success'))
