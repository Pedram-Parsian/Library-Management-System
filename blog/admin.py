from django.contrib import admin
from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug']

    class Meta:
        model = models.Post


@admin.register(models.PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(models.PostTag)
class PostTagAdmin(admin.ModelAdmin):
    ...


@admin.register(models.PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    ...
