from .base import *

DEBUG = True

ALLOWED_HOSTS.append('*')

INSTALLED_APPS.insert(5, 'livereload')

INSTALLED_APPS.append('debug_toolbar')

# email backend for local testing only
EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"
)

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

MIDDLEWARE.append('livereload.middleware.LiveReloadScript')
