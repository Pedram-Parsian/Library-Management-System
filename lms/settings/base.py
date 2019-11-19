import os
from .secrets import (
    _SECRET_KEY,
    _DB_PASSWORD,
    _RECAPTCHA_PUBLIC_KEY,
    _RECAPTCHA_PRIVATE_KEY,
    _SMS_USERNAME,
    _SMS_PASSWORD,
    _SMS_PHONE_NUMBER,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = _SECRET_KEY

DEBUG = False

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.postgres',
    'rest_framework',
    'widget_tweaks',
    'import_export',
    'captcha',
    'bootstrap_modal_forms',
    'ckeditor',
    'users.apps.UsersConfig',
    'core.apps.CoreConfig',
    'documents.apps.DocumentsConfig',
    'circulation.apps.CirculationConfig',
    'blog.apps.BlogConfig',
    'accounting.apps.AccountingConfig',
    'reports.apps.ReportsConfig',
    'ticketing.apps.TicketingConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'lms.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'lms',
        'USER': 'djangodbman',
        'PASSWORD': _DB_PASSWORD,
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'users.User'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'assets')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

LOGIN_REDIRECT_URL = 'home'

LOGIN_URL = 'users:login'

LOGOUT_URL = 'users:logout'

CHARFIELD_MAX_LENGTH = 250

SLUGFIELD_MAX_LENGTH = 250

TEXTFIELD_MAX_LENGTH = 500

DEFAULT_ACTIVATION_DATE = 7

# Google reCAPTCHA:
RECAPTCHA_PUBLIC_KEY = _RECAPTCHA_PUBLIC_KEY

RECAPTCHA_PRIVATE_KEY = _RECAPTCHA_PRIVATE_KEY

RECAPTCHA_DOMAIN = 'www.recaptcha.net'

# settings for ticket attachments:

MAX_ATTACHMENTS = 5

MAX_ATTACHMENT_SIZE = 5e+6  # in bytes

VALID_ATTACHMENT_EXTENSIONS = {
    '.png': 'image/png',
    '.jpeg': 'image/jpeg',
    '.pdf': 'application/pdf',
}

DEFAULT_POST_NEW_DAYS = 7

# Library Information (used in reports)
LIBRARY_INFORMATION = {
    'NAME': 'MIT Library',
    'DATE_ESTABLISHED': 'Jan 1952',
}

# SMS sending panel information:
SMS_USERNAME = _SMS_USERNAME
SMS_PASSWORD = _SMS_PASSWORD
SMS_PHONE_NUMBER = _SMS_PHONE_NUMBER
