from django.urls import path, re_path

from . import views

app_name = 'users'
urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/comments', views.ProfileReviewsView.as_view(), name='reviews'),
    path('profile/tickets', views.ProfileTicketsView.as_view(), name='tickets'),
    path('profile/ticket/<int:pk>/', views.ProfileTicketView.as_view(), name='ticket_detail'),
    path('profile/reserves', views.ProfileReservesView.as_view(), name='reserves'),
    path('profile/issues', views.ProfileIssuesView.as_view(), name='issues'),
    path('profile/reserves/delete/<int:pk>', views.ProfileReserveDelete.as_view(), name='delete_reserve'),
    path('profile/reviews/delete/<int:pk>', views.ProfileReviewDeleteView.as_view(), name='delete_review'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signup-successful', views.SignupCompleteView.as_view(), name='signup_complete'),
    path('email-activation/resend/', views.ResendActivationEmail.as_view(), name='resend_activation_email'),
    path('email-activation/resend-successful', views.ResendActivationEmailSuccessful.as_view(),
         name='resend_activation_email_successful'),
    re_path(r'^email-activation/(?P<key>[0-9A-Za-z]+)/$', views.AccountEmailActivationView.as_view(),
            name='email_activation'),
]
