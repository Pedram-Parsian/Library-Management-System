from . import base

base.DEBUG = True

base.ALLOWED_HOSTS.append('*')

base.INSTALLED_APPS.insert(5, 'livereload')

base.INSTALLED_APPS.append('debug_toolbar')

# email backend for local testing only
base.EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"
)

base.MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

base.MIDDLEWARE.append('livereload.middleware.LiveReloadScript')
