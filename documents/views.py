from django.views.generic import ListView, DetailView

from . import models


class DocumentListView(ListView):
    template_name = 'documents/list.html'
    model = models.Document
    paginate_by = 100

    def get_queryset(self):
        search_field = self.request.GET.get('search_field')
        search_query = self.request.GET.get('search_query')
        available_only = True if 'available_only' in self.request.GET else False
        search_dict = {}

        if available_only:
            search_dict['status'] = models.Document.AVAILABLE
        if search_query:
            if search_field == 'title':
                search_dict['title__search'] = search_query
            elif search_field == 'author':
                search_dict['authors__name__search'] = search_query
            elif search_field == 'publisher':
                search_dict['publisher__name__search'] = search_query

        return models.Document.objects.filter(**search_dict)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'documents'
        return context


class DocumentDetailView(DetailView):
    model = models.Document

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = models.Comment.objects.filter(document=self.get_object(),
                                                            status=models.Comment.APPROVED)
        context['navbar'] = 'documents'
        return context
