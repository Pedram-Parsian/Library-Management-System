from django.contrib import admin
from . import models


@admin.register(models.Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Reply)
class ReplyAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Ticket)
class TicketAdmin(admin.ModelAdmin):
    ...
