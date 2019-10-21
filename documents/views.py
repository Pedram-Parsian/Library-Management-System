from django.views.generic import ListView, DetailView

from . import models


class DocumentListView(ListView):
    template_name = 'documents/list.html'
    model = models.Document
    paginate_by = 10

    def get_queryset(self):
        search_field = self.request.GET.get('search_field')
        search_query = self.request.GET.get('search_query')

        # todo switch to postgresql to work:
        if search_query:
            if search_field == 'title':
                return models.Document.objects.filter(title__search=search_query)
            elif search_field == 'author':
                return models.Document.objects.filter(authors__name__search=search_query)
            elif search_field == 'publisher':
                return models.Document.objects.filter(publications__name__search=search_query)

        return models.Document.objects.all()

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
