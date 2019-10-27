from django.urls import path

from . import views

app_name = 'documents'
urlpatterns = [
    path('list/', views.DocumentListView.as_view(), name='list'),
    path('<slug:slug>/', views.DocumentDetailView.as_view(), name='detail'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author'),
    path('translator/<int:pk>/', views.TranslatorDetailView.as_view(), name='translator'),
    path('editor/<int:pk>/', views.EditorDetailView.as_view(), name='editor'),
    path('publisher/<int:pk>/', views.PublisherDetailView.as_view(), name='publisher'),
    path('age-classification/<int:pk>/', views.AgeClassificationDetailView.as_view(), name='age-classification'),
]
