from django.views.generic import ListView

from . import models


class DocumentListView(ListView):
    template_name = 'documents/list.html'
    model = models.Document

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'documents'
        return context
