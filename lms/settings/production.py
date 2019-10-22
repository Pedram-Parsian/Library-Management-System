from .secrets import _EMAIL_HOST_PASSWORD

# email back-end for production
# todo change to internal server SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'pedram.parsian@gmail.com'
EMAIL_HOST_PASSWORD = _EMAIL_HOST_PASSWORD
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Pedram Parsian <Pedram.Parsian@gmail.com>'
ADMINS = (
    ('Pedram Parsian', 'Pedram.Parsian@gmail.com'),
)
MANAGERS = ADMINS
