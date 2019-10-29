from django.views.generic import ListView, DetailView

from . import models


class DocumentListView(ListView):
    template_name = 'documents/list.html'
    model = models.Document
    paginate_by = 100

    def get_queryset(self):
        sort_by = self.request.GET.get('sort_by')
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

        if sort_by:
            if sort_by == '1':
                sort_by = 'title'
            elif sort_by == '2':
                sort_by = 'publisher__name'
            elif sort_by == '3':
                sort_by = '-rating'
            elif sort_by == '4':
                sort_by = '???'  # todo complete this sorting
        else:
            sort_by = 'id'

        return models.Document.objects.order_by(sort_by).filter(**search_dict)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'documents'
        context['sort_by'] = self.request.GET.get('sort_by')
        return context


class DocumentDetailView(DetailView):
    template_name = 'documents/document_detail.html'
    model = models.Document

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = models.DocumentComment.objects.filter(document=self.get_object(),
                                                                    status=models.DocumentComment.APPROVED)
        context['navbar'] = 'documents'
        return context


class AuthorDetailView(DetailView):
    template_name = 'documents/author_detail.html'
    model = models.Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'documents'
        return context


class TranslatorDetailView(DetailView):
    template_name = 'documents/translator_detail.html'
    model = models.Translator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'documents'
        return context


class EditorDetailView(DetailView):
    template_name = 'documents/editor_detail.html'
    model = models.Editor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'documents'
        return context


class PublisherDetailView(DetailView):
    template_name = 'documents/publisher_detail.html'
    model = models.Publisher

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'documents'
        return context


class AgeClassificationDetailView(DetailView):
    template_name = 'documents/age_classification_detail.html'
    model = models.AgeClassification

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'documents'
        return context
