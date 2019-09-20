import hashlib
import urllib

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('email_activated', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    email_activated = models.BooleanField('user\'s email confirmation', default=False)
    notifications = models.ManyToManyField('Notification', verbose_name='user\'s notifications', blank=True)
    avatar = models.ImageField(upload_to='user-avatars/', blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def get_avatar(self):
        if self.avatar:
            return self.avatar
        return self._get_gravatar_url()

    def _get_gravatar_url(self):
        encoded_email_address = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
        gravatar_size = urllib.parse.urlencode({'d': 'identicon', 's': '35'})
        return f'https://www.gravatar.com/avatar/{encoded_email_address}?{gravatar_size}'


class Notification(models.Model):
    # todo Complete this class :)
    pass

# todo add EmailActivationClass
