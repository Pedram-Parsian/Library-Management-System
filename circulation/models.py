from django.db import models
from django.conf import settings
from users.models import Member
from documents.models import Document
from users.models import User, Member
from accounting.models import Payment

# Terminology:
# issue (checkout)
# return
# renew
# reserve


class Issue(models.Model):
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    document = models.ForeignKey(Document, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(blank=True, null=True)
    # after the member had returned the book, this will be filled:
    returned_date = models.DateTimeField(blank=True, null=True)
    # and there may be a fine:
    # it's considered as ManyToManyField because there may be a OVERDUE & DAMAGE fine at the same time
    fines = models.ManyToManyField('Fine', blank=True)

    @property
    def has_renews(self):
        return True if self.renew_set else False

    @property
    def is_returned(self):
        return True if self.returned_date else False


class Fine(models.Model):
    OVERDUE = 10
    DAMAGE = 20
    OTHER = 30
    REASON_CHOICES = (
        (OVERDUE, 'Overdue'),
        (DAMAGE, 'Damage'),
        (OTHER, 'Other'),
    )
    reason = models.IntegerField(choices=REASON_CHOICES)
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    amount = models.IntegerField()
    staff = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, blank=True, null=True)
    description = models.TextField(max_length=settings.TEXTFIELD_MAX_LENGTH, blank=True, null=True)

    @property
    def has_payed(self):
        return True if self.payment else False

    def __str__(self):
        return f'{self.amount} for {self.member} by{self.staff} @ {self.timestamp}'


class Reserve(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    available_since = models.DateTimeField(blank=True, null=True)
    # after the member has submitted the issue, it will be stored here:
    # todo check if CASCADE is the right choice here
    issue = models.ForeignKey(Issue, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} reserve {self.document} @ {self.timestamp}'


class Renew(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()

    def __str__(self):
        return f'Renew for issue <{self.issue_id}> from {self.timestamp} to {self.due_date}'
