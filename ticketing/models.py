from django.core.validators import MaxValueValidator
from django.db import models
from django.conf import settings

from users.models import Member, User


class Ticket(models.Model):
    # Priorities:
    LOW = 10
    NORMAL = 20
    HIGH = 30
    CRITICAL = 40

    # Status:
    OPEN = 10
    CLOSED = 20

    # Departments:
    ADMINISTRATION = 10
    CIRCULATION_SERVICES = 20
    OTHER = 30

    PRIORITY_CHOICES = (
        (LOW, 'Low'),
        (NORMAL, 'Normal'),
        (HIGH, 'High'),
        (CRITICAL, 'Critical'),
    )
    STATUS_CHOICES = (
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
    )
    DEPARTMENT_CHOICES = (
        (ADMINISTRATION, 'Administration'),
        (CIRCULATION_SERVICES, 'Circulation Services'),
        (OTHER, 'Other'),
    )
    subject = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=NORMAL)
    department = models.IntegerField(choices=DEPARTMENT_CHOICES)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=OPEN)
    date_opened = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.get_status_display()}]-[{self.get_priority_display()}] <{self.subject}>'


class Reply(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=1000)
    rating = models.PositiveSmallIntegerField(validators=(MaxValueValidator(5),))

    def __str__(self):
        return f'{self.user.get_full_name()} replied to [{self.ticket.get_priority_display()}] <{self.ticket.subject}>'


class Attachment(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='ticket_attachments/')

    def __str__(self):
        return f'Attachment for <{self.reply}>'
