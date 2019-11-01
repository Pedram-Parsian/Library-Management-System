from django.contrib import admin
from . import models

admin.site.register(models.Ticket)
admin.site.register(models.Reply)
admin.site.register(models.Attachment)
