from django.urls import path
from . import views

app_name = 'ticketing'
urlpatterns = [
    path('create_ticket/', views.TicketCreateView.as_view(), name='create_ticket'),
]
