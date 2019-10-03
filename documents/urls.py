from django.urls import path

from . import views

app_name = 'documents'
urlpatterns = [
    path('list/', views.DocumentListView.as_view(), name='list')
]