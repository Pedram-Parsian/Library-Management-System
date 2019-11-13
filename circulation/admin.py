from django.contrib import admin
from . import models


@admin.register(models.Issue)
class IssueAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Fine)
class FineAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Reserve)
class ReserveAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Renew)
class RenewAdmin(admin.ModelAdmin):
    ...
