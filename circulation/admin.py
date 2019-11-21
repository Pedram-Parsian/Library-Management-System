from django.contrib import admin
from . import models


@admin.register(models.Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['document', 'member', 'timestamp', 'status']
    raw_id_fields = ['document', 'member']
    date_hierarchy = 'timestamp'


@admin.register(models.Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = ['issue', 'amount', 'timestamp']
    raw_id_fields = ['issue']
    date_hierarchy = 'timestamp'


@admin.register(models.Reserve)
class ReserveAdmin(admin.ModelAdmin):
    list_display = ['member', 'document', 'status']
    raw_id_fields = ['document', 'member']
    date_hierarchy = 'timestamp'


@admin.register(models.Renew)
class RenewAdmin(admin.ModelAdmin):
    list_display = ['issue', 'due_date']
    raw_id_fields = ['issue']
    date_hierarchy = 'timestamp'
