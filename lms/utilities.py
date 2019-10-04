import urllib
import hashlib
import random
import string
from django.utils.text import slugify


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    class_ = instance.__class__
    qs_exists = class_.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = f"{slug}-{random_string_generator(size=5)}"
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_gravatar_url(email):
    encoded_email_address = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    gravatar_size = urllib.parse.urlencode({'d': 'identicon', 's': '35'})
    return f'https://www.gravatar.com/avatar/{encoded_email_address}?{gravatar_size}'


def convert_range(old_min, old_max, new_min, new_max, value):
    old_range = old_max - old_min
    new_range = new_max - new_min
    return (((value - old_min) * new_range) / old_range) + new_min
