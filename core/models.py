from django.db import models
from django.conf import settings
from users.models import User
from lms.utilities import get_gravatar_url


class BaseComment(models.Model):
    APPROVED = 10
    REFUSED = 20
    WAITING = 30
    STATUS_CHOICES = (
        (APPROVED, 'Approved'),
        (REFUSED, 'Refused'),
        (WAITING, 'Waiting...')
    )

    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField(max_length=600)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=WAITING)

    def get_avatar(self):
        if not self.user:
            return get_gravatar_url(self.email)
        return self.user.get_avatar()

    def get_info(self):
        if self.user:
            return self.user.first_name, self.user.last_name
        else:
            return self.name, None

    class Meta:
        abstract = True
