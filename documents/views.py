from django.shortcuts import render
from django.views.generic import ListView

from . import models


class DocumentListView(ListView):
    template_name = 'documents/list.html'
    model = models.Document
