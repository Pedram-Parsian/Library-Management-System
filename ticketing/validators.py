import os
import magic
from django.conf import settings
from django.core.exceptions import ValidationError


# todo use django.core.validators -> FileExtensionValidator
def file_extension_validator(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = settings.VALID_ATTACHMENT_EXTENSIONS.keys()
    if ext.lower() not in valid_extensions:
        raise ValidationError(u'File extension not supported!')


def file_type_validator(value):
    file_mime = magic.from_buffer(value.file.read(), mime=True)
    if file_mime not in settings.VALID_ATTACHMENT_EXTENSIONS.values():
        raise ValidationError('File type not supported!')


def form_file_size_validator(value):
    if value.size > settings.MAX_ATTACHMENT_SIZE:
        raise ValidationError('File is too large!')
