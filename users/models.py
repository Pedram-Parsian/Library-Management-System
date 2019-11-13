from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db.models import Q
from django.template.loader import get_template
from django.utils import timezone
from django.urls import reverse
from django.db import models


class User(AbstractUser):
    # todo user should be notified if there is any new notification!
    MALE = 1
    FEMALE = 2
    OTHER = 3
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    )
    date_of_birthday = models.DateField(blank=True, null=True)
    identification_code = models.CharField(max_length=10, unique=True)
    gender = models.IntegerField(choices=GENDER_CHOICES)
    father_name = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH, blank=True, null=True)
    place_of_birthday = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH, blank=True, null=True)
    is_member = models.BooleanField(default=False)
    # overriding the default email field, because that's not unique:
    email = models.EmailField('email address', blank=True, null=True, unique=True)
    email_activated = models.BooleanField('user\'s email confirmation', default=False)
    avatar = models.ImageField(upload_to='user-avatars/', blank=True, null=True)
    REQUIRED_FIELDS = ['first_name', 'last_name', 'identification_code', 'gender', 'email']

    def get_avatar(self, size):
        if self.avatar:
            return self.avatar
        return self._get_gravatar_url(size)

    def _get_gravatar_url(self, size):
        from lms.utilities import get_gravatar_url
        return get_gravatar_url(self.email, size)

    def __str__(self):
        return f'{self.get_full_name()} ({self.username})'


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    groups = models.ManyToManyField('Group', blank=True)
    membership = models.ForeignKey('Membership', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return f'{self.user.get_full_name()} ({self.user.username})'


class Group(models.Model):
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    @property
    def member_count(self):
        return self.member_set.count()

    def __str__(self):
        if self.parent:
            return f'{self.title} ({self.member_count} members) --> {self.parent}'
        return f'{self.title} ({self.member_count} members)'


class Membership(models.Model):
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH, blank=True, null=True)
    total_issues = models.PositiveIntegerField(null=True, blank=True)
    total_concurrent_issues = models.PositiveIntegerField(null=True, blank=True)
    total_reserves = models.PositiveIntegerField(null=True, blank=True)
    total_renews = models.PositiveIntegerField(null=True, blank=True)
    max_continuous_renews = models.PositiveIntegerField(null=True, blank=True)
    issue_duration = models.DurationField(null=True, blank=True)
    renew_duration = models.DurationField(null=True, blank=True)
    description = models.TextField(max_length=settings.TEXTFIELD_MAX_LENGTH, blank=True, null=True)
    fine_amount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'Membership {self.title}'


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)
    text = models.TextField(max_length=settings.TEXTFIELD_MAX_LENGTH)

    def __str__(self):
        return f'<{self.title}> {self.text} for <{self.user}>'


class EmailActivationQuerySet(models.query.QuerySet):
    def confirmable(self):
        # todo with this custom QuerySet, we can call EmailActivation.objects.all().confirmable() and get all confirmable objects,so, we can have "unactivated accounts & count of them" in the admin using this method!
        start_range = timezone.now() - timedelta(days=settings.DEFAULT_ACTIVATION_DAYS or 7)
        end_range = timezone.now()
        return self.filter(
            is_activated=False,
            forced_expired=False,
        ).filter(
            timestamp__gt=start_range,
            timestamp__lte=end_range,
        )


class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQuerySet(self.model, using=self._db)

    def confirmable(self):
        return self.get_queryset().confirmable()

    def email_exists(self, email):
        return self.get_queryset().filter(Q(email=email) | Q(user__email=email)).filter(is_activated=False)


class EmailActivation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    key = models.CharField(max_length=120, null=True, blank=True)
    is_activated = models.BooleanField(default=False)
    forced_expired = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    objects = EmailActivationManager()

    def __str__(self):
        return f'[{self.is_activated}] {self.email}'

    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable()
        if qs.exists():
            return True
        return False

    def activate(self):
        if self.can_activate():
            user = self.user
            user.email_activated = True
            user.save()
            # todo Post activation user signal -> send another email (welcome email! + offer)
            self.is_activated = True
            self.save()
            return True
        return False

    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False

    def send_activation_email(self):
        if not self.is_activated and not self.forced_expired:
            if self.key:
                path = settings.BASE_URL + reverse('email_activation', kwargs={'key': self.key})
                context = {
                    'path': path,
                    'email': self.email,
                }
                txt_ = get_template('users/emails/confirm_email.txt').render(context)
                html_ = get_template('users/emails/confirm_email.html').render(context)
                subject = 'Confirm Your Email'
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [self.email]
                sent_mail = send_mail(subject, txt_, from_email, recipient_list, html_message=html_,
                                      fail_silently=False)
                return sent_mail
        return False
