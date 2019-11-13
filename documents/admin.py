from django.contrib import admin

from . import models


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ('document', 'member',)


@admin.register(models.Document)
class DocumentAdmin(admin.ModelAdmin):
    ...


@admin.register(models.DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Translator)
class TranslatorAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Editor)
class EditorAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Publisher)
class PublisherAdmin(admin.ModelAdmin):
    ...


@admin.register(models.AgeClassification)
class AgeClassificationAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Building)
class BuildingAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Floor)
class FloorAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Repository)
class RepositoryAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Rack)
class RackAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Row)
class RowAdmin(admin.ModelAdmin):
    ...
