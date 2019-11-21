from django.urls import path

from . import views

app_name = 'reports'
urlpatterns = [
    path('document/<int:id>/', views.DocumentReport.as_view(), name='document'),
    path('documents/', views.DocumentsReport.as_view(), name='documents'),
    path('member/<int:pk>/card/', views.MemberCard.as_view(), name='member_card'),
    path('member/<int:id>/', views.MemberReport.as_view(), name='member'),
    path('members/', views.MembersReport.as_view(), name='members'),
    path('members/cards/', views.MembersCards.as_view(), name='members_cards'),
    path('issue_receipt/<int:id>/', views.IssueReceiptReport.as_view(), name='issue_receipt'),
    path('issues/', views.IssuesReport.as_view(), name='issues'),
    path('renew_receipt/<int:id>/', views.RenewReceiptReport.as_view(), name='renew_receipt'),
    path('renews/', views.RenewsReport.as_view(), name='renews'),
    path('reserve_receipt/<int:id>/', views.ReserveReceiptReport.as_view(), name='reserve_receipt'),
    path('reserves/', views.ReservesReport.as_view(), name='reserves'),
]
