from django.contrib import admin

from . import models

admin.site.register(models.Document)
admin.site.register(models.DocumentType)
admin.site.register(models.Author)
admin.site.register(models.Translator)
admin.site.register(models.Language)
admin.site.register(models.Publisher)
admin.site.register(models.AgeClassification)
admin.site.register(models.Review)
admin.site.register(models.Building)
admin.site.register(models.Floor)
admin.site.register(models.Repository)
admin.site.register(models.Rack)
admin.site.register(models.Row)
