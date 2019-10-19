from django.urls import path

from . import views


app_name = 'circulation'
urlpatterns = [
    path('reserve/', views.ReserveView.as_view(), name='reserve'),
]