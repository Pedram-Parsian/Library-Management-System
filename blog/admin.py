from django.contrib import admin
from . import models


class PostAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug']

    class Meta:
        model = models.Post


admin.site.register(models.Post, PostAdmin)
admin.site.register(models.PostCategory)
admin.site.register(models.PostTag)
admin.site.register(models.PostComment)
