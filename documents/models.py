from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from django.db.models import Count
from django.urls import reverse
from users.models import Member


class BasePerson(models.Model):
    name = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)

    def get_documents_count(self):
        return self.document_set.count()

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Review(models.Model):
    APPROVED = 10
    REFUSED = 20
    WAITING = 30
    STATUS_CHOICES = (
        (APPROVED, 'Approved'),
        (REFUSED, 'Refused'),
        (WAITING, 'Waiting...')
    )
    document = models.ForeignKey('Document', on_delete=models.PROTECT)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, blank=True, null=True)
    rating = models.PositiveSmallIntegerField(validators=(MaxValueValidator(5),))
    text = models.TextField(max_length=600, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=WAITING)

    def __str__(self):
        return f'"{self.member.user.get_full_name()}" on document "{self.document.title}"'


class Document(models.Model):
    AVAILABLE = 10  # the document is ready to be checked out. reserving is not possible
    RESERVED = 20  # document is available in the library, but it's reserved. checkout for others is not allowed.
    LOANED = 30  # document is out of library, may also be reserved too (edge case)
    LOST = 40  # document is lost and not available at all, but keep info for refrencing
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
    publisher = models.ForeignKey('Publisher', on_delete=models.PROTECT, null=True, blank=True)
    age_classification = models.ForeignKey('AgeClassification', on_delete=models.PROTECT, blank=True, null=True)
    location = models.ForeignKey('Row', on_delete=models.PROTECT, blank=True, null=True)
    call_no = models.CharField(max_length=20, blank=True, null=True)
    authors = models.ManyToManyField('Author', blank=True)
    translators = models.ManyToManyField('Translator', blank=True)
    editors = models.ManyToManyField('Editor', blank=True)
    number_of_pages = models.IntegerField(blank=True, null=True)
    published_year = models.IntegerField(blank=True, null=True)
    # todo signal for re-calculating the rating whenever members add/remove review
    rating = models.DecimalField(max_digits=2, decimal_places=1,
                                 validators=(MinValueValidator(0), MaxValueValidator(5)))
    description = models.TextField(max_length=settings.TEXTFIELD_MAX_LENGTH, blank=True, null=True)
    summary = models.TextField(max_length=settings.TEXTFIELD_MAX_LENGTH, blank=True, null=True)

    # todo generate call_no based on row (location) + id + hash + ...
    # todo generate slug

    def get_document_count(self):
        """
        find the number of the same document in the library
        """
        ...

    def get_absolute_url(self):
        return reverse('documents:detail', args=[self.slug])

    @staticmethod
    def recalculate_rating(document_id):
        document_reviews = Review.objects.filter(document_id=document_id)
        document_average_rating = sum(document_reviews.values_list('rating', flat=True)) / document_reviews.count()
        document = Document.objects.get(id=document_id)
        document.rating = document_average_rating
        document.save()

    def set_status(self):
        """
        Set the document status based on issues & reserves status
        First, we prevent further overhead if the document was marked as LOST.
        After that, we check the following things in order:
            *) if there is an _active_ issue for the document,
                we set the expected_status to LOANED
                **) If there is any renews on top of the issue, the Issue object's status
                    will consider that.
            *) otherwise, if there is an _active_ reserve for the document,
                we set the expected_status to RESERVED
            *) if none of the above situations happen,
                we set the document status to AVAILABLE
        Finally, if the current documents status was different from the expected status,
        we will change the status and save that.
        """
        from circulation.models import Issue, Reserve
        if self.status == Document.LOST:
            return

        # in the following `if`, I'm assuming that the DB data is **valid**
        # (e.g. there may be more than one _active_ issue for the document)
        if self.issue_set.filter(status__in=(Issue.PENDING, Issue.PENDING_OVERDUE)).exists():
            expected_status = Document.LOANED
        else:
            if self.reserve_set.filter(status=Reserve.AVAILABLE):
                expected_status = Document.RESERVED
            else:
                expected_status = Document.AVAILABLE

        if self.status != expected_status:
            self.status = expected_status
            self.save()

    @staticmethod
    def get_top_ten_documents():
        return Document.objects.filter(status__in=[Document.AVAILABLE, Document.RESERVED, Document.LOANED]).annotate(
            total_issues=Count('issue')).annotate(total_reserves=Count('reserve')).order_by('-total_issues',
                                                                                            '-total_reserves',
                                                                                            '-rating')[:10]

    def __str__(self):
        return f'{self.title} ({self.call_no})'


class DocumentType(models.Model):
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)
    is_digital = models.BooleanField(default=False)

    def get_documents_count(self):
        return self.document_set.count()

    def __str__(self):
        return f'{self.title} ({"digital" if self.is_digital else "physical"})'


class Language(models.Model):
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)
    native_name = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH, blank=True, null=True)

    def get_documents_count(self):
        return self.document_set.count()

    def __str__(self):
        if self.native_name:
            return f'{self.title} ({self.native_name})'
        return self.title


class Author(BasePerson):
    def get_absolute_url(self):
        return reverse('documents:author', args=[self.id])


class Translator(BasePerson):
    def get_absolute_url(self):
        return reverse('documents:translator', args=[self.id])


class Editor(BasePerson):
    def get_absolute_url(self):
        return reverse('documents:editor', args=[self.id])


class Building(models.Model):
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)

    def get_floors_count(self):
        return self.floor_set.count()

    def __str__(self):
        return f'Building {self.title}'


class Floor(models.Model):
    building = models.ForeignKey(Building, on_delete=models.PROTECT)
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)

    def get_repositories_count(self):
        return self.repository_set.count()

    def __str__(self):
        return f'Floor {self.title}'


class Repository(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.PROTECT)
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)

    def get_racks_count(self):
        return self.rack_set.count()

    def __str__(self):
        return f'Repository {self.title}'


class Rack(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.PROTECT)
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)

    def get_rows_count(self):
        return self.row_set.count()

    def __str__(self):
        return f'Rack {self.title}'


class Row(models.Model):
    rack = models.ForeignKey(Rack, on_delete=models.PROTECT)
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)

    def get_documents_count(self):
        return self.document_set.count()

    def __str__(self):
        return f'Row {self.title}'


class Publisher(models.Model):
    name = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)
    date_of_establishment = models.DateField(blank=True, null=True)
    refer_to = models.ForeignKey('self', blank=True, null=True, on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse('documents:publisher', args=[self.id])

    def get_documents_count(self):
        return self.document_set.count()

    def __str__(self):
        if self.refer_to:
            return f'{self.name} ({self.refer_to.name})'
        return f'{self.name}'


class AgeClassification(models.Model):
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)
    min_age = models.PositiveSmallIntegerField()

    def get_absolute_url(self):
        return reverse('documents:age-classification', args=[self.id])

    def get_documents_count(self):
        return self.document_set.count()

    def __str__(self):
        return f'{self.title} (from {self.min_age} years old)'
