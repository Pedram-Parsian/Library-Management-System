from django.contrib import admin

from . import models

admin.site.register(models.User)
admin.site.register(models.Member)
admin.site.register(models.Membership)
admin.site.register(models.Notification)
admin.site.register(models.EmailActivation)
