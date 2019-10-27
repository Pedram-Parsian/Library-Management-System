from django.urls import path

from . import views

app_name = 'documents'
urlpatterns = [
    path('list/', views.DocumentListView.as_view(), name='list'),
    path('<slug:slug>/', views.DocumentDetailView.as_view(), name='detail'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author'),
]
