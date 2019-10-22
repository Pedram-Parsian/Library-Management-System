from django.urls import path

from . import views


app_name = 'reports'
urlpatterns = [
    path('members/', views.MembersList.as_view(), name='members_list'),
    path('members/cards', views.MembersCardList.as_view(), name='members_card_list'),
    path('members/cards/pdf', views.generate_pdf, name='members_card_list_pdf'),
]
