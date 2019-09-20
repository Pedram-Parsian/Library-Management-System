from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('', views.AboutView.as_view(), name='about'),
    path('', views.ContactView.as_view(), name='contact'),
]
