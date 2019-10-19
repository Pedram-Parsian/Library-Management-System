from django.contrib import admin
from . import models


admin.site.register(models.Issue)
admin.site.register(models.Fine)
admin.site.register(models.Reserve)
admin.site.register(models.Renew)