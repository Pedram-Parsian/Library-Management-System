from django.urls import path, re_path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.BlogHomeView.as_view(), name='blog'),
    path('like/<int:post_id>', views.LikePostView, name='like_post'),
    path('<slug:slug>/', views.BlogDetailView.as_view(), name='post'),
    re_path(r'^archive/(?P<year>[0-9]{4})-(?P<month>[0-9]{2})/$', views.BlogArchiveView.as_view(), name='archive'),
    path('tag/<slug:tag>/', views.BlogTagView.as_view(), name='blog_tag'),
    path('category/<slug:category>/', views.BlogCategoryView.as_view(), name='blog_category'),
]
