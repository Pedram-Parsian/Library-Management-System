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
    document = models.ForeignKey('Document', on_delete=models.CASCADE)

    def __str__(self):
        name, family = self.get_info()
        if self.parent:
            return f'"{name} {family}" on "{self.document.title}" (child comment)'
        return f'"{name} {family}" on post "{self.document.title}"'


class Document(models.Model):
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)
    slug = models.SlugField(max_length=settings.SLUGFIELD_MAX_LENGTH, blank=True, unique=True)
    DDC = models.CharField(max_length=10, blank=True, null=True)
    LCC = models.CharField(max_length=10, blank=True, null=True)
    NBN = models.CharField(max_length=10, blank=True, null=True)
    ISBN = models.CharField(max_length=10, blank=True, null=True)
    active = models.BooleanField(default=True)
    checkoutable = models.BooleanField(default=True)
    reservable = models.BooleanField(default=True)
    price = models.IntegerField(blank=True, null=True)
    edition = models.PositiveSmallIntegerField(blank=True, null=True)
    copies = models.PositiveIntegerField(blank=True, null=True)
    # I use document_type instead of 'type' because type is a python keyword!
    document_type = models.ForeignKey('DocumentType', on_delete=models.CASCADE, blank=True, null=True)
    language = models.ForeignKey('Language', on_delete=models.CASCADE, blank=True, null=True)
    publications = models.ManyToManyField('Publication', blank=True)
    age_classification = models.ForeignKey('AgeClassification', on_delete=models.CASCADE, blank=True, null=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    authors = models.ManyToManyField('Author', blank=True)
    translators = models.ManyToManyField('Translator', blank=True)
    editors = models.ManyToManyField('Editor', blank=True)
    number_of_pages = models.IntegerField(blank=True, null=True)
    description = models.TextField(max_length=settings.TEXTFIELD_MAX_LENGTH, blank=True, null=True)

    def is_available(self):
        # see if book is available for reserve or checkout
        pass

    def get_status(self):
        # find out whether the book is in the library or not
        return 'In the library'

    def __str__(self):
        return self.title


class Author(BasePerson):
    ...


class Translator(BasePerson):
    ...


class Editor(BasePerson):
    ...


class DocumentType(models.Model):
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)
    is_digital = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} ({"digital" if self.is_digital else "physical"})'


class Location(models.Model):
    building = models.ForeignKey('Building', on_delete=models.CASCADE)
    floor = models.ForeignKey('Floor', on_delete=models.CASCADE)
    # section = models.ForeignKey('Section', on_delete=models.CASCADE)

    def __str__(self):
        # todo generate a call number based on the data
        return f'{self.building} --> {self.floor}'


class Building(models.Model):
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)

    def __str__(self):
        return self.title


class Floor(models.Model):
    building = models.ForeignKey('Building', on_delete=models.CASCADE)
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)

    def __str__(self):
        return f'{self.title} (in {self.building})'


class Language(models.Model):
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)
    native_name = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH, blank=True, null=True)

    def __str__(self):
        if self.native_name:
            return f'{self.title} ({self.native_name})'
        return self.title


class Publication(models.Model):
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)
    date_of_establishment = models.DateField(blank=True, null=True)
    refer_to = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.refer_to:
            return f'{self.title} ({self.refer_to.title})'
        return f'{self.title}'


class AgeClassification(models.Model):
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)
    min_age = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.title} (from {self.min_age} years old)'

