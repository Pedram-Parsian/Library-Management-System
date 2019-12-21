from django.contrib import admin

from . import models


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['member', 'document', 'get_status_display', 'date_added']
    readonly_fields = ('document', 'member',)


@admin.register(models.Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'publisher']


@admin.register(models.DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_documents_count', 'is_digital']


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_documents_count']


@admin.register(models.Translator)
class TranslatorAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_documents_count']


@admin.register(models.Editor)
class EditorAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_documents_count']


@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['title', 'native_name', 'get_documents_count']


@admin.register(models.Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name', 'date_of_establishment', 'refer_to', 'get_documents_count']


@admin.register(models.AgeClassification)
class AgeClassificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'min_age', 'get_documents_count']


@admin.register(models.Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_floors_count']


@admin.register(models.Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ['title', 'building', 'get_repositories_count']


@admin.register(models.Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'floor', 'get_racks_count']


@admin.register(models.Rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ['title', 'repository', 'get_rows_count']


@admin.register(models.Row)
class RowAdmin(admin.ModelAdmin):
    list_display = ['title', 'rack', 'get_documents_count']
