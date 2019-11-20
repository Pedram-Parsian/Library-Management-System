from django.contrib import admin
from django.utils import timezone

from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_status_display']
    actions = ['make_published']

    def make_published(self, request, queryset):
        posts_updated = queryset.update(status=models.Post.PUBLISHED, date_published=timezone.now())
        message = '1 post was' if posts_updated == 1 else f'{posts_updated} posts were'
        self.message_user(request, f'{message} successfully marked as published.')

    make_published.short_description = 'Mark selected posts as published'


@admin.register(models.PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_posts_count']


@admin.register(models.PostTag)
class PostTagAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_posts_count']


@admin.register(models.PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ['member', 'post', 'get_status_display']
