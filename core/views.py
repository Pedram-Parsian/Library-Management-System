from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from documents.models import Document
from . import forms


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'home'
        context['top_ten_documents'] = Document.get_top_ten_documents()
        # context['recent_posts'] = Post.objects.all()[:3]
        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'about'
        return context


class ContactView(FormView):
    template_name = 'core/contact.html'
    success_url = reverse_lazy('contact')
    form_class = forms.ContactForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'CONTACT'
        return context

    def form_valid(self, form):
        form.send_mail()
        messages.success(self.request, 'Your message has been sent. Thanks!')
        return super(ContactView, self).form_valid(form)
