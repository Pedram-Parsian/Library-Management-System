from django.urls import path

from . import views


app_name = 'circulation'
urlpatterns = [
    path('reserve/<int:id>/', views.ReserveView.as_view(), name='reserve'),
]