from django.db import models
from django.conf import settings
from core.models import BaseComment


class BasePerson(models.Model):
    name = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Comment(BaseComment):
    document = models.ForeignKey('Document', on_delete=models.PROTECT)

    def __str__(self):
        name, family = self.get_info()
        if self.parent:
            return f'"{name} {family}" on "{self.document.title}" (child comment)'
        return f'"{name} {family}" on document "{self.document.title}"'


class Document(models.Model):
    AVAILABLE = 10  # the document is ready to be checked out. reserving is not possible
    RESERVED = 20  # document is available in the library, but it's reserved. checkout for others is not allowed.
    LOANED = 30  # document is out of library, may also be reserved too (edge case)
    LOST = 40 # document is lost and not available at all, but keep info for refrencing
    DOCUMENT_STATUS = (
        (AVAILABLE, 'Available'),
        (RESERVED, 'Reserved'),
        (LOANED, 'Loaned'),
        (LOST, 'Lost'),
    )
    # todo write pre-save and post-save signals to change the status of the document automatically in the related models
    # example: when checking out, reserving, etc.
    status = models.IntegerField(choices=DOCUMENT_STATUS, default=AVAILABLE)
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)
    # I use document_type instead of 'type' because type is a python keyword!
    document_type = models.ForeignKey('DocumentType', on_delete=models.PROTECT, blank=True, null=True)
    slug = models.SlugField(max_length=settings.SLUGFIELD_MAX_LENGTH, blank=True, unique=True)
    # todo check the length of DDC, LCC, NBN, ISBN
    DDC = models.CharField(max_length=10, blank=True, null=True)
    LCC = models.CharField(max_length=10, blank=True, null=True)
    NBN = models.CharField(max_length=10, blank=True, null=True)
    ISBN = models.CharField(max_length=13, blank=True, null=True)
    active = models.BooleanField(default=True)
    checkoutable = models.BooleanField(default=True)
    reservable = models.BooleanField(default=True)
    price = models.IntegerField(blank=True, null=True)
    edition = models.PositiveSmallIntegerField(blank=True, null=True)
    copies = models.PositiveIntegerField(blank=True, null=True)
    language = models.ForeignKey('Language', on_delete=models.PROTECT, blank=True, null=True)
    publications = models.ManyToManyField('Publication', blank=True)
    age_classification = models.ForeignKey('AgeClassification', on_delete=models.PROTECT, blank=True, null=True)
    location = models.ForeignKey('Row', on_delete=models.PROTECT)
    call_no = models.CharField(max_length=20, blank=True, null=True)
    authors = models.ManyToManyField('Author', blank=True)
    translators = models.ManyToManyField('Translator', blank=True)
    editors = models.ManyToManyField('Editor', blank=True)
    number_of_pages = models.IntegerField(blank=True, null=True)
    description = models.TextField(max_length=settings.TEXTFIELD_MAX_LENGTH, blank=True, null=True)

    # todo generate call_no based on row (location) + id + hash + ...
    # todo generate slug

    def get_document_count(self):
        """
        find the number of the same document in the library
        """
        ...

    def __str__(self):
        return f'{self.title} ({self.call_no})'


class DocumentType(models.Model):
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)
    is_digital = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} ({"digital" if self.is_digital else "physical"})'


class Language(models.Model):
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)
    native_name = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH, blank=True, null=True)

    def __str__(self):
        if self.native_name:
            return f'{self.title} ({self.native_name})'
        return self.title


class Author(BasePerson):
    ...


class Translator(BasePerson):
    ...


class Editor(BasePerson):
    ...


class Building(models.Model):
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)

    def __str__(self):
        return f'Building {self.title}'


class Floor(models.Model):
    building = models.ForeignKey(Building, on_delete=models.PROTECT)
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)

    def __str__(self):
        return f'Floor {self.title}'


class Repository(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.PROTECT)
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)

    def __str__(self):
        return f'Repository {self.title}'


class Rack(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.PROTECT)
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)

    def __str__(self):
        return f'Rack {self.title}'


class Row(models.Model):
    rack = models.ForeignKey(Rack, on_delete=models.PROTECT)
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)

    def __str__(self):
        return f'Row {self.title}'


class Publication(models.Model):
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)
    date_of_establishment = models.DateField(blank=True, null=True)
    refer_to = models.ForeignKey('self', blank=True, null=True, on_delete=models.PROTECT)

    def __str__(self):
        if self.refer_to:
            return f'{self.title} ({self.refer_to.title})'
        return f'{self.title}'


class AgeClassification(models.Model):
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)
    min_age = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.title} (from {self.min_age} years old)'

