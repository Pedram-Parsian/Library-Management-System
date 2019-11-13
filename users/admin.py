from django.contrib import admin
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'username', 'get_gender_display', 'identification_code', 'is_member']


@admin.register(models.Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'get_member_identification_code', 'membership']

    def get_member_identification_code(self, member):
        return member.user.identification_code


@admin.register(models.Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['title', 'total_issues', 'total_renews', 'total_reserves']


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    ...


@admin.register(models.EmailActivation)
class EmailActivationAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'member_count', 'parent']
