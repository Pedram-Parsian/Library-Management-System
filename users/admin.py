from django.contrib import admin
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Member)
class MemberAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Membership)
class MembershipAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    ...


@admin.register(models.EmailActivation)
class EmailActivationAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    ...
