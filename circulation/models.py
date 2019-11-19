from django.db import models
from django.conf import settings
from django.utils import timezone

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
    PENDING = 10
    PENDING_OVERDUE = 20
    DONE = 30
    DONE_OVERDUE = 40
    ISSUE_STATUS = (
        (PENDING, 'Pending'),
        (PENDING_OVERDUE, 'Pending Overdue'),
        (DONE, 'Done'),
        (DONE_OVERDUE, 'Done Overdue'),
    )
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    document = models.ForeignKey(Document, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(blank=True, null=True)
    # after the member had returned the book, this will be filled:
    returned_date = models.DateTimeField(blank=True, null=True)
    # todo remove the possible "-----" choice in admin
    status = models.PositiveSmallIntegerField(choices=ISSUE_STATUS, blank=True)

    def set_status(self):
        if not self.pk:
            self.status = Issue.PENDING
        else:
            # the max_due_date will have either the *most far* due date or the instance due_date itself,
            # if there is not any renews for the issue:
            max_due_date = self.renew_set.order_by(
                '-due_date').first().due_date if self.renew_set.exists() else self.due_date
            if self.returned_date:
                # user has returned the document
                if self.returned_date > max_due_date:
                    self.status = Issue.DONE_OVERDUE
                else:
                    self.status = Issue.DONE
            else:
                # user has not returned document
                if timezone.now() >= max_due_date:
                    self.status = Issue.PENDING_OVERDUE
                else:
                    self.status = Issue.PENDING

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
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    reason = models.IntegerField(choices=REASON_CHOICES)
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
    """
    possible status of a reserve:
    1. book is not available yet --> waiting...(+ estimated availability date): forced_remove=False available_since=None
     and issue_id=None
    2. book is available --> available: forced_remove=False and available_since!=None and issue_id=None
     and <due date has not passed>
    3. book was available and member submit checkout before due date --> proceed: issue_id!=None
    4. book was available but member didn't submit checkout before due date --> expired: forced_remove=False and
      available_since!=None and issue_id=None and <due date has passed>
    5. the reservation has been forced removed by staff or admin --> not accepted: forced_remove=True
    ?. if the member remove the reservation himself/herself, we will actually remove the row at DB
    """
    # warning: do not change the following numbers, or change them as well in the corresponding template!
    WAITING = 10  # possible to remove by member
    AVAILABLE = 20  # possible to remove by member
    PROCEED = 30
    EXPIRED = 40
    FORCED_EXPIRED = 50
    RESERVE_STATUS = (
        (WAITING, 'Waiting...'),
        (AVAILABLE, 'Available'),
        (PROCEED, 'Proceed'),
        (EXPIRED, 'Expired'),
        (FORCED_EXPIRED, 'Expired by staff'),
    )
    # using a post-save signal, we will automatically fill the status field:
    # todo write that signal!!
    status = models.IntegerField(choices=RESERVE_STATUS, null=True, blank=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    available_since = models.DateTimeField(blank=True, null=True)
    # after the member has submitted the issue, it will be stored here:
    # todo check if CASCADE is the right choice here
    issue = models.ForeignKey(Issue, blank=True, null=True, on_delete=models.CASCADE)
    description = models.TextField(max_length=settings.TEXTFIELD_MAX_LENGTH, blank=True, null=True)

    def set_status(self):
        ...

    def __str__(self):
        return f'{self.member} reserve {self.document} @ {self.timestamp} - {self.get_status_display()}'


class Renew(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()

    def __str__(self):
        return f'Renew for issue <{self.issue_id}> from {self.timestamp} to {self.due_date}'
